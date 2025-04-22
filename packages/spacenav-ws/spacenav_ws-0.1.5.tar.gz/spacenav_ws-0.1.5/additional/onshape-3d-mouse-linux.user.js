// ==UserScript==
// @name         Onshape 3D‑Mouse on Linux (in‑page patch)
// @description  Fake the platform property on 'navigator' to convince Onshape it's running under Windows. This causes it to ask for information on https://127.51.68.120:8181/3dconnexion/nlproxy so that a 3d mouse can be connected.
// @match        https://cad.onshape.com/documents/*
// @run-at       document-start
// @grant        none
// @version 0.0.1
// @license MIT
// @namespace https://greasyfork.org/users/1460506
// ==/UserScript==

Object.defineProperty(Navigator.prototype, 'platform', { get: () => 'Win32' });
console.log('[Onshape patch] navigator.platform →', navigator.platform);
