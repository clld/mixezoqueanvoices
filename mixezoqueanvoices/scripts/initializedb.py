import collections

from pycldf import Sources
from clldutils.misc import nfilter
from clld.cliutil import Data, bibtex2source
from clld.db.meta import DBSession
from clld.db.models import common
from clld.lib import bibtex
from clld_audio_plugin.models import Counterpart
from clld_audio_plugin.util import form2audio
from clldutils import licenses
from clldutils.color import qualitative_colors
from pyglottolog import Glottolog

import mixezoqueanvoices
from mixezoqueanvoices import models


def main(args):
    assert args.glottolog, 'The --glottolog option is required!'
    license = licenses.find(args.cldf.properties['dc:license'])
    assert license and license.id.startswith('CC-')

    data = Data()
    ds = data.add(
        common.Dataset,
        mixezoqueanvoices.__name__,
        id=mixezoqueanvoices.__name__,
        name="Mixe-Zoquean Voices",
        domain='mixezoqueanvoices.clld.org',
        publisher_name="Max Planck Institute for the Science of Human History",
        publisher_place="Jena",
        publisher_url="http://www.shh.mpg.de",
        license=license.url,
        jsondata={
            'license_icon': '{}.png'.format(
                '-'.join([p.lower() for p in license.id.split('-')[:-1]])),
            'license_name': license.name},
    )

    contrib = data.add(
        common.Contribution,
        None,
        id='cldf',
        name=args.cldf.properties.get('dc:title'),
        description=args.cldf.properties.get('dc:bibliographicCitation'),
    )
    data.add(common.Contributor, 'kondic', id='kondic', name='Ana Kondic')
    data.add(common.Contributor, 'gray', id='gray', name='Russell Gray')
    DBSession.add(common.ContributionContributor(
        contribution=contrib,
        contributor=data['Contributor']['kondic'],
    ))
    for i, ed in enumerate(['kondic', 'gray']):
        data.add(common.Editor, ed, dataset=ds, contributor=data['Contributor'][ed], ord=i)

    ancestors = collections.defaultdict(list)
    gl = Glottolog(args.glottolog)
    lnames = {}
    for lang in args.cldf.iter_rows('LanguageTable', 'id', 'glottocode', 'name', 'latitude', 'longitude'):
        lnames[lang['id']] = lang['name']
        glang = None
        if lang['glottocode']:
            glang = gl.languoid(lang['glottocode'])
            lineage = [i[0] for i in glang.lineage]
            if 'Mixe-Zoque' in lineage:
                ancestors[lang['id']].append('Protomixezoque')
            if 'Mixe' in lineage:
                ancestors[lang['id']].append('Protomixe')
            if 'Oaxaca Mixe' in lineage:
                ancestors[lang['id']].append('Protooaxacamixe')
        if not glang:
            assert lang['name'] == 'Nizaviguiti'
        data.add(
            models.Variety,
            lang['id'],
            id=lang['id'],
            name=lang['name'],
            latitude=lang['latitude'],
            longitude=lang['longitude'],
            glottocode=lang['glottocode'],
            description=lang['LongName'],
            subgroup=glang.lineage[1][0] if glang and len(glang.lineage) > 1 else None,
        )
    colors = dict(zip(
        set(l.subgroup for l in data['Variety'].values()),
        qualitative_colors(len(set(l.subgroup for l in data['Variety'].values())))))
    for l in data['Variety'].values():
        l.jsondata = dict(color=colors[l.subgroup].replace('#', ''))

    for rec in bibtex.Database.from_file(args.cldf.bibpath, lowercase=True):
        data.add(common.Source, rec.id, _obj=bibtex2source(rec))

    refs = collections.defaultdict(list)

    # Store proto-forms for later lookup:
    proto_forms = collections.defaultdict(lambda: collections.defaultdict(list))
    for form in args.cldf.iter_rows('FormTable', 'id', 'form', 'languageReference', 'parameterReference'):
        if form['languageReference'].startswith('Proto'):
            proto_forms[form['languageReference']][form['parameterReference']].append(form['form'])

    for param in args.cldf.iter_rows('ParameterTable', 'id', 'concepticonReference', 'name'):
        proto = collections.OrderedDict()
        for lid, forms in proto_forms.items():
            f = forms.get(param['id'])
            if f:
                proto[lnames[lid]] = f
        data.add(
            models.Concept,
            param['id'],
            id=param['id'],
            name='{} [{}]'.format(param['name'], param['id'].split('_')[0]),
            concepticon_id=param['concepticonReference'],
            concepticon_gloss=param['Concepticon_Gloss'],
            description=param['Spanish_Gloss'],
            jsondata=dict(reconstructions=proto),
        )

    f2a = form2audio(args.cldf)
    for form in args.cldf.iter_rows('FormTable', 'id', 'form', 'languageReference', 'parameterReference', 'source'):
        assert not (form['form'] == '►' and not f2a.get(form['id']))
        vsid = (form['languageReference'], form['parameterReference'])
        vs = data['ValueSet'].get(vsid)
        if not vs:
            vs = data.add(
                common.ValueSet,
                vsid,
                id='-'.join(vsid),
                language=data['Variety'][form['languageReference']],
                parameter=data['Concept'][form['parameterReference']],
                contribution=contrib,
            )
        for ref in form.get('source', []):
            sid, pages = Sources.parse(ref)
            refs[(vsid, sid)].append(pages)
        proto = collections.OrderedDict()
        for lid in ancestors.get(form['languageReference'], []):
            f = proto_forms[lid].get(form['parameterReference'])
            if f:
                proto[lnames[lid]] = f
        data.add(
            Counterpart,
            form['id'],
            id=form['id'],
            name=form['form'],
            valueset=vs,
            audio=f2a.get(form['id']),
            jsondata=dict(reconstructions=proto),
        )

    for (vsid, sid), pages in refs.items():
        DBSession.add(common.ValueSetReference(
            valueset=data['ValueSet'][vsid],
            source=data['Source'][sid],
            description='; '.join(nfilter(pages))
        ))


def prime_cache(args):
    """If data needs to be denormalized for lookup, do that here.
    This procedure should be separate from the db initialization, because
    it will have to be run periodically whenever data has been updated.
    """
