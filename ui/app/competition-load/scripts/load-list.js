/* load-list.js - Load concurrent list
 * 
 * Agility Teams Manager - Classements par équipe pour sportscanins.fr 
 * Copyright (C) 2021  Virinas-code
 *
 *  This program is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program.  If not, see <https://www.gnu.org/licenses/>. 
 */
let progressBar = document.getElementById("loading-bar");
progressBar.hidden = false;

fetch(`/api/${competitionId}/load`).then(
    function(response) {
        progressBar.hidden = true;
        // window.location.href = `/app/${competitionId}`;
    }
)