<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "parameters" %>
<%block name="title">${_('Parameter')} ${ctx.name}</%block>



<h2>${_('Parameter')} ${ctx.name}</h2>

% if ctx.description:
    <p><strong>Spanish:</strong> ${ctx.description}</p>
% endif

% if ctx.jsondata['reconstructions']:
    <h4>Reconstructions [<a href="${req.route_url('source', id='Wichmann1995')}">Wichmann 1995</a>]</h4>
    <dl class="dl-horizontal">
        % for l, forms in ctx.jsondata['reconstructions'].items():
            <dt>${l}:</dt>
            <dd>${', '.join(forms)}</dd>
        % endfor
    </dl>
% endif

<div style="clear: both"/>
% if map_ or request.map:
${(map_ or request.map).render()}
% endif

${request.get_datatable('values', h.models.Value, parameter=ctx).render()}
