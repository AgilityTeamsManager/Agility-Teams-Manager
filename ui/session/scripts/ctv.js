/* CTV script. */
// Agility Teams Manager - CTV script.
// Copyright (C) 2022  Virinas-code

// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.

// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.

// You should have received a copy of the GNU General Public License
// along with this program.  If not, see <https://www.gnu.org/licenses/>.

var elements = document.querySelectorAll("ctv-element");
var items = document.querySelectorAll("ctv-item");
var parent = document.querySelector("ctv-list");
var searchBar = document.querySelector("input");
var selectedElement;
var selectedItem = document.querySelector("ctv-default");

function click_event(e) {
    console.debug(this);
    console.debug(Array.prototype.indexOf.call(parent.children, this));
    if (selectedItem) {selectedItem.removeAttribute("class");}
    if (selectedElement) {selectedElement.removeAttribute("class");}
    selectedElement = this;
    selectedElement.setAttribute("class", "focus");
    selectedItem = items[Array.prototype.indexOf.call(parent.getElementsByTagName("ctv-element"), this)];
    selectedItem.setAttribute("class", "focus");
}

function focus(e) {
    e.preventDefault();
    console.debug("e");
    this.blur();
    searchBar.focus();
}

for (var element of elements) {
    element.addEventListener("click", click_event, false);
}

document.querySelectorAll("input")[1].addEventListener("focus", focus)