import collections
import pathlib

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
from clldutils.misc import slug
from cldfbench import get_dataset
from pyglottolog import Glottolog
from sqlalchemy import func
from sqlalchemy.orm import joinedload
from nameparser import HumanName

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
        publisher_name="Max Planck Institute for Evolutionary Anthropology",
        publisher_place="Leipzig",
        publisher_url="https://www.eva.mpg.de",
        license=license.url,
        jsondata={
            'license_icon': '{}.png'.format(
                '-'.join([p.lower() for p in license.id.split('-')[:-1]])),
            'license_name': license.name},
    )

    r = get_dataset('mixezoqueanvoices', ep='lexibank.dataset')
    authors, _ = r.get_creators_and_contributors()
    for ord, author in enumerate(authors):
        cid = slug(HumanName(author['name']).last)
        c = data.add(
            common.Contributor,
            cid,
            id=cid,
            name=author['name'],
            description=author.get('description'),
            jsondata=None,
        )

    contribs = collections.defaultdict(lambda: collections.defaultdict(list))
    for c in args.cldf.iter_rows('contributions.csv'):
        for role in ['phonetic_transcriptions', 'recording', 'sound_editing', 'reconstruction']:
            if c[role] is None:
                continue
            for name in c[role].split(' and '):
                if name:
                    cid = slug(HumanName(name).last)
                    contribs[c['Language_ID']][cid].append(role)

    data.add(
        common.Contributor,
        'wichmann',
        id='wichmann',
        name='Søren Wichmann',
        description='Reconstructions of Proto-Forms',
        jsondata=dict(img=None),
    )

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
            sgroup = glang.lineage[1][0] if glang and len(glang.lineage) > 1 else None
        if not glang:
            if lang['name'] == 'Nizaviguiti':
                ancestors[lang['id']].append('Protomixe')
                sgroup = 'Mixe'
            elif lang['name'] == 'Tapalapa':
                ancestors[lang['id']].append('Protomixezoque')
                sgroup = 'Zoque'

        contrib = data.add(
            common.Contribution,
            lang['id'],
            id=lang['id'],
            name='Wordlist for {}'.format(lang['name']),
        )
        if lang['id'] in contribs:
            for cid, roles in contribs[lang['id']].items():
                DBSession.add(common.ContributionContributor(
                    contribution=contrib,
                    contributor=data['Contributor'][cid],
                    jsondata=dict(roles=roles),
                ))

        data.add(
            models.Variety,
            lang['id'],
            id=lang['id'],
            name=lang['name'],
            latitude=lang['latitude'],
            longitude=lang['longitude'],
            glottocode=lang['glottocode'],
            description=lang['LongName'],
            subgroup=sgroup,
        )

    contrib = data.add(
        common.Contribution,
        None,
        id='cldf',
        name=args.cldf.properties.get('dc:title'),
        description=args.cldf.properties.get('dc:bibliographicCitation'),
    )

    colors = dict(zip(
        set(lg.subgroup for lg in data['Variety'].values()),
        qualitative_colors(len(set(lg.subgroup for lg in data['Variety'].values())))))
    for lg in data['Variety'].values():
        lg.jsondata = dict(color=colors[lg.subgroup].replace('#', ''))

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

    for i, ed in enumerate(['kondic', 'gray']):
        data.add(common.Editor, ed, dataset=ds, contributor=data['Contributor'][ed], ord=i)

    f2a = form2audio(args.cldf, 'audio/mpeg')
    for form in args.cldf.iter_rows('FormTable', 'id', 'form', 'languageReference', 'parameterReference', 'source', 'comment', 'segments'):
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
            description=' '.join(form['segments']),
            valueset=vs,
            audio=f2a.get(form['id']),
            jsondata=dict(reconstructions=proto, comment=form['comment']),
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

    for cpt in DBSession.query(
        models.Concept, func.count(models.Concept.pk))\
            .filter(common.Value.name != '►')\
            .join(common.ValueSet).join(common.Value).group_by(
                models.Concept.pk, common.Parameter.pk):
        cpt[0].count_lexemes = cpt[1]

    for language in DBSession.query(common.Language).options(
            joinedload(common.Language.valuesets, common.ValueSet.references)):
        language.count_concepts = len(language.valuesets)
        language.count_lexemes = len(DBSession.query(common.Value.id)
                                     .filter(common.ValueSet.language_pk == language.pk)
                                     .filter(common.Value.name != '►')
                                     .join(common.ValueSet).all())
        language.count_soundfiles = len(DBSession.query(Counterpart.id)
                                        .filter(common.ValueSet.language_pk == language.pk)
                                        .filter(Counterpart.audio.isnot(None))
                                        .join(common.ValueSet).all())
