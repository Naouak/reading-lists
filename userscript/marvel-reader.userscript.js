// ==UserScript==
// @name         Reading List Updater for read.marvel.com
// @namespace    https://github.com/Naouak/Reading-lists
// @version      0.1
// @description  Update your reading history on your reading list automatically on read.marvel.com
// @author       Naouak
// @match        https://read.marvel.com/
// @grant        none
// ==/UserScript==

(function() {
    'use strict';
    const api_url = 'http://localhost:3000';
    const orig = window.rocket.models.controlsModel.toggleShowNextComic.bind(window.rocket.models.controlsModel);
    window.rocket.models.controlsModel.toggleShowNextComic = function(...args){
        window.open(api_url+'/mark-as-read/marvel/'+window.rocket.models.model.attributes.issue_meta.catalog_id);
        return orig(...args);
    };
})();