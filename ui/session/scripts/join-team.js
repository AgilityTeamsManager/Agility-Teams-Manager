/* Join team script. */
// Agility Teams Manager - Join team script.
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

var items = document.querySelectorAll("ctv-item"); // All the items

function click_on_join(e) {
    console.log(this.parentNode.parentNode.querySelector("header > div > span").textContent);
}

function setup() {
    /* Add event listener to items. */
    var button;
    for (var item of items) {
        console.log(item);
        button = item.querySelector("button");
        if (button && !("dimmed" in button.getAttribute("class").split(" "))) {
            button.addEventListener("click", click_on_join);
        }
    }
}

setup();