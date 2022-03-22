/* Error script. */
// Agility Teams Manager - Error script.
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
var errorsBox = document.querySelector("#errors");

function error(message) {
    var errorObject = document.createElement("div");
    errorObject.textContent = "Erreur : " + message;
    errorsBox.appendChild(errorObject);
    setTimeout(function() {errorObject.hidden = true;}, 2000)
}