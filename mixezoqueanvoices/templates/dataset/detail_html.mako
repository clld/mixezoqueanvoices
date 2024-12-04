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
    <div style="float:left;margin:10px;margin-top:60px">
        <h4>${_('Statistics')}</h4>
        <table class="table table-condensed">
            <tbody>
            <tr>
                <th>${_('Languages')}</th>
                <td class="right">${'{:,}'.format(stats['language'])}</td>
            </tr>
            <tr>
                <th>${_('Parameters')}</th>
                <td class="right">${'{:,}'.format(stats['parameter'])}</td>
            </tr>
            <tr>
                <th>${_('Values')}</th>
                <td class="right">${'{:,}'.format(stats['value'])}</td>
            </tr>
            </tbody>
        </table>
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
        Ana Kondić, Paul Heggarty, & Darja Dërmaku-Appelganz. (2020). Mixe-Zoquean Voices (Version 1.0.1) [Data set]. Zenodo. http://doi.org/10.5281/zenodo.4350652
        <br>
        <a href="https://doi.org/10.5281/zenodo.4350652"><img src="https://zenodo.org/badge/DOI/10.5281/zenodo.4350652.svg" alt="DOI"></a>
    </blockquote>
</div>
