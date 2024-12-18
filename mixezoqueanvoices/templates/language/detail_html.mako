<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "languages" %>
<%block name="title">${_('Language')} ${ctx.name}</%block>

<h2>${_('Language')} ${ctx.name}</h2>

${request.get_datatable('values', h.models.Value, language=ctx).render()}

<%def name="sidebar()">
    ${util.codes(ctx)}
    <% contributors = context.get('contributors', []) %>
    % if len(contributors) > 0:
        <h4>${_('Contributors')}</h4>
        <ul class="unstyled">
            % for c in contributors:
                <li>
                    <strong>${c[0]}</strong>: ${', '.join([r.replace('_', ' ') for r in c[1]])}
                </li>
            % endfor
        </ul>
    % endif
    % if ctx.subgroup:
        <strong style="font-size: 1.2em;">${_('Subgroup')}</strong>: ${ctx.subgroup}
    % endif
    <br /><br />
    ${util.language_meta()}
</%def>
