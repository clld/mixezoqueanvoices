from clld.db.meta import DBSession
from clld.db.models.common import ContributionContributor, Contributor
from clld import RESOURCES


def language_detail_html(context=None, request=None, **kw):
    return {
        'contributors': get_contributors(context),
    }


def get_contributors(context):
    res = []
    for c in DBSession.query(Contributor.name, ContributionContributor)\
            .join(Contributor)\
            .filter(ContributionContributor.contribution_pk == context.pk):
        res.append((c[0], c[1].jsondata['roles']))
    return res


def dataset_detail_html(context=None, request=None, **kw):
    return dict(
        stats=context.get_stats(
            [rsc for rsc in RESOURCES if rsc.name in ['language', 'parameter', 'value']])
    )
