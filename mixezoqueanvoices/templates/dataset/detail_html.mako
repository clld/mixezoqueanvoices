<%inherit file="../home_comp.mako"/>

<%block name="head">
    <style>
        .dt-before-table {visibility: hidden; height: 0;}
        .dataTables_info {visibility: hidden; height: 0;}
        .dataTables_paginate {visibility: hidden; height: 0;}
    </style>
</%block>

<%def name="sidebar()">
    <div class="well">
        <img src="${req.static_url('mixezoqueanvoices:static/ico-MixeZoque.jpg')}" class="img-rounded">
    </div>
</%def>

<div id="with-background">
    <h2>${_('Welcome to')} Mixe-Zoquean Voices</h2>

    <p class="lead">
        ${_('Mixe-Zoquean Voices presents primary recordings of languages from the Mixe-Zoque language family.')}
    </p>

    <p>
        ${_('Cite the Mixe-Zoquean Voices dataset as')}
    </p>
    <blockquote>
        Ana Kondić, Paul Heggarty, & Darja Dërmaku-Appelganz. (2020). Mixe-Zoquean Voices (Version 1.0) [Data set]. Zenodo. http://doi.org/10.5281/zenodo.4327418
        <br>
        <a href="https://doi.org/10.5281/zenodo.4327418"><img src="https://zenodo.org/badge/DOI/10.5281/zenodo.4327418.svg" alt="DOI"></a>
    </blockquote>
</div>
