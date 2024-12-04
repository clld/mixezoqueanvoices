from clld.db.models import common
from clld.db.util import get_distinct_values
from clld.web import datatables
from clld.web.datatables.base import LinkCol, Col, LinkToMapCol
from clld.web.datatables.contributor import Contributors
from clld.web.util import concepticon
from clld.web.util.glottolog import url
from clld.web.util.helpers import map_marker_img
from clld.web.util.htmllib import HTML
from clld_audio_plugin.datatables import AudioCol

from sqlalchemy.orm import joinedload

from mixezoqueanvoices import models


class SubgroupCol(Col):
    def format(self, item):
        try:
            return HTML.div(map_marker_img(self.dt.req, item), ' ', HTML.span(item.subgroup))
        except Exception:
            return HTML.div(map_marker_img(self.dt.req, item.valueset.language), ' ', HTML.span(item.valueset.language.subgroup))


class MZGlottologCol(Col):
    def format(self, item):
        if item.glottocode:
            return HTML.a(item.glottocode, href=url(item.glottocode))
        return ''


class Languages(datatables.Languages):
    def col_defs(self):
        return [
            LinkCol(self, 'name', sTitle=self.req._('Name')),
            MZGlottologCol(self, 'Glottocode', model_col=models.Variety.glottocode),
            SubgroupCol(
                self,
                'subgroup',
                sTitle=self.req._('Subgroup'),
                model_col=models.Variety.subgroup,
                choices=get_distinct_values(models.Variety.subgroup)),
            Col(self, 'count_concepts',
                sTitle=self.req._('# concepts'),
                sTooltip=self.req._('number of concepts per language'),
                model_col=models.Variety.count_concepts),
            Col(self, 'count_lexemes',
                sTitle=self.req._('# words'),
                sTooltip=self.req._('number of words per language'),
                model_col=models.Variety.count_lexemes),
            Col(self, 'count_soundfiles',
                sTitle=self.req._('# audio'),
                sTooltip=self.req._('number of sound files per language'),
                model_col=models.Variety.count_soundfiles),
            Col(self,
                'latitude',
                sDescription='<small>The geographic latitude</small>'),
            Col(self,
                'longitude',
                sDescription='<small>The geographic longitude</small>'),
            LinkToMapCol(self, 'm'),
        ]


class ReconstructionsCol(Col):
    __kw__ = dict(bSearchable=False, bSortable=False)

    def format(self, item):
        return HTML.ul(
            *[HTML.li('{}: {}'.format(k, ', '.join(v)))
              for k, v in item.jsondata['reconstructions'].items()],
            **{'class': 'unstyled'})


class CommentCol(Col):
    __kw__ = dict(bSearchable=False, bSortable=False)

    def format(self, item):
        return item.jsondata['comment']


class WordLinkCol(LinkCol):
    def format(self, item):
        if item.name and item.name != '►':
            return super(WordLinkCol, self).format(item)


class Words(datatables.Values):
    def base_query(self, query):
        if not any([self.language, self.parameter, self.contribution]):
            return query\
                .join(common.ValueSet)\
                .join(common.Parameter)\
                .join(common.Language)\
                .options(
                    joinedload(common.Value.valueset).joinedload(common.ValueSet.parameter),
                    joinedload(common.Value.valueset).joinedload(common.ValueSet.language)
                )
        else:
            return datatables.Values.base_query(self, query)

    def get_default_options(self):
        opts = super(datatables.Values, self).get_default_options()
        if not self.language and not self.parameter:
            opts['aaSorting'] = [[0, 'asc'], [3, 'asc'], [2, 'asc']]
        elif self.parameter:
            opts['aaSorting'] = [[1, 'asc'], [0, 'asc'], [3, 'asc']]
        else:
            opts['aaSorting'] = [[0, 'asc'], [3, 'asc']]
        return opts

    def col_defs(self):
        res = []
        if self.language:
            res.extend([
                LinkCol(
                    self,
                    'gloss_en',
                    sTitle=self.req._('English'),
                    model_col=common.Parameter.name,
                    get_object=lambda v: v.valueset.parameter),
                Col(self,
                    'gloss_en',
                    sTitle=self.req._('Spanish'),
                    get_object=lambda v: v.valueset.parameter,
                    model_col=common.Parameter.description,
                    format=lambda i: i.valueset.parameter.description),
            ])
        elif self.parameter:
            res.extend([
                LinkCol(self, 'language', sTitle=self.req._('Language'),
                        get_object=lambda v: v.valueset.language,
                        model_col=common.Language.name),
                SubgroupCol(
                    self,
                    'subgroup',
                    sTitle=self.req._('Subgroup'),
                    model_col=models.Variety.subgroup,
                    choices=get_distinct_values(models.Variety.subgroup)),
                # Col(self,
                #     'desc',
                #     sTitle=self.req._('Location'),
                #     get_object=lambda v: v.valueset.language,
                #     model_col=common.Language.description,
                #     ),
            ])
        else:
            res.extend([
                LinkCol(
                    self,
                    'gloss_en',
                    sTitle=self.req._('English'),
                    model_col=common.Parameter.name,
                    get_object=lambda v: v.valueset.parameter),
                Col(self,
                    'gloss_en',
                    sTitle=self.req._('Spanish'),
                    get_object=lambda v: v.valueset.parameter,
                    model_col=common.Parameter.description,
                    format=lambda i: i.valueset.parameter.description),
                LinkCol(self, 'language', sTitle=self.req._('Language'),
                        get_object=lambda v: v.valueset.language,
                        model_col=common.Language.name),
                SubgroupCol(
                    self,
                    'subgroup',
                    sTitle=self.req._('Subgroup'),
                    model_col=models.Variety.subgroup,
                    choices=get_distinct_values(models.Variety.subgroup)),
                # Col(self,
                #     'desc',
                #     sTitle=self.req._('Location'),
                #     get_object=lambda v: v.valueset.language,
                #     model_col=common.Language.description,
                #     ),
                ])
        res.append(WordLinkCol(self, 'name', sTitle=self.req._('Word')))
        res.append(Col(self, 'description', sTitle=self.req._('Segments')))
        res.append(CommentCol(self, 'comment', sTitle='Comment'))
        res.append(ReconstructionsCol(self, 'description', sTitle=self.req._('Reconstruction')))
        res.append(AudioCol(self, '#'))
        return res


class ConcepticonCol(Col):
    def format(self, item):
        return concepticon.link(self.dt.req, item.concepticon_id, label=item.concepticon_gloss)


class Concepts(datatables.Parameters):
    def col_defs(self):
        return [
            LinkCol(self, 'name', sTitle=self.req._('English')),
            Col(self, 'description', sTitle='Spanish'),
            Col(self, 'count_lexemes',
                sTitle=self.req._('# words'),
                sTooltip=self.req._('number of words per concept'),
                model_col=models.Concept.count_lexemes),
            ConcepticonCol(self, 'concepticon'),
        ]


class MZContributors(Contributors):
    def col_defs(self):
        return [
            Col(self, 'name', sTitle=self.req._('Name')),
            Col(self, 'description', sTitle=self.req._('Role')),
        ]


def includeme(config):
    config.register_datatable('languages', Languages)
    config.register_datatable('parameters', Concepts)
    config.register_datatable('values', Words)
    config.register_datatable('contributors', MZContributors)
