<%inherit file="home_comp.mako"/>
<%namespace name="mpg" file="clldmpg_util.mako"/>

<h3>${_('Downloads')}</h3>

<div class="alert alert-info">
    <p>
        ${_('Mixe-Zoquean Voices serves the latest')}
        ${h.external_link('https://github.com/lexibank/mixezoqueanvoices/releases', label=_('released version'))}
        ${_('of data curated at')}
        ${h.external_link('https://github.com/lexibank/mixezoqueanvoices', label='lexibank/mixezoqueanvoices')}.
        ${_('All released version are accessible via')} <br/>
        <a href="https://doi.org/10.5281/zenodo.4327417">
            <img src="https://zenodo.org/badge/DOI/10.5281/zenodo.4327417.svg" alt="DOI">
        </a>
        <br/>
        ${_('on ZENODO as well')}.
    </p>
</div>
