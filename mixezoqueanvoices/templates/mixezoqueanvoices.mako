<%inherit file="app.mako"/>

##
## define app-level blocks:
##
<%block name="header">
    ##<a href="${request.route_url('dataset')}">
    ##    <img src="${request.static_url('mixezoqueanvoices:static/header.gif')}"/>
    ##</a>
        <style>
        #html {
            min-height: 99%; /* or whatever your desired height is */
            height: 99%; /* or whatever your desired height is */
            min-width: 99%; /* or whatever your desired width is */
            width: 99%; /* or whatever your desired width is */
        }

    </style>
</%block>

${next.body()}
