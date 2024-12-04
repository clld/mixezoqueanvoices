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
        <script src="${req.static_url('mixezoqueanvoices:static/L.Control.Resizer.js')}"></script>
        <link rel="stylesheet" href="${req.static_url('mixezoqueanvoices:static/L.Control.Resizer.css')}">
</%block>

${next.body()}
