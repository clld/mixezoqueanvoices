<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "lexemes" %>
<%block name="title">${_('Lexeme')} ${ctx.name}</%block>

<h2>${_('Value')}: ${ctx.name}</h2>

<div style='float:left'>
    <dl>
        <dt>${_('Segments')}:</dt>
        <dd>${ctx.description}</dd>
        <dt>${_('Language')}:</dt>
        <dd>${h.link(request, ctx.valueset.language)}</dd>
        <dt>${_('Meaning')}:</dt>
        <dd>${h.link(request, ctx.valueset.parameter)}</dd>
        % if ctx.valueset.references:
        <dt>${_('References')}:</dt>
        <dd>${h.linked_references(request, ctx.valueset)|n}</dd>
        % endif
    </dl>
</div>

% if ctx.jsondata['comment']:
<div class="container" style="overflow:auto;width:100%;margin-bottom:30px">
    <b>Notes: </b>${ctx.jsondata['comment'] | n}
</div>
% endif

% if ctx.jsondata['reconstructions'] and len(ctx.jsondata['reconstructions']) > 0:
<div class="container" style="overflow:auto;width:100%;margin-bottom:30px">
    <b>${_('Reconstructions')}:</b>
    <ul>
    % for k, v in ctx.jsondata['reconstructions'].items():
        <li>${k | n}: ${', '.join(v) | n}
    </ul>
    % endfor
</div>
% endif

% if ctx.sentence_assocs:
<h3>${_('Sentences')}</h3>
<ol>
    % for a in ctx.sentence_assocs:
    <li>
        % if a.description:
        <p>${a.description}</p>
        % endif
        ${h.rendered_sentence(a.sentence)}
        % if a.sentence.references:
        <p>See ${h.linked_references(request, a.sentence)|n}</p>
        % endif
    </li>
    % endfor
</ol>
% endif