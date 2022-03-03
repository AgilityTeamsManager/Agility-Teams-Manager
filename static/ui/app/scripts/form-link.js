/* form-link.js - Utilisty to send form on link click.
 * Copyright (C) 2022  Virinas-code
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
let form = document.getElementById("form-link");
let links = document.getElementsByTagName("a");

for (var i = 0; i < links.length; i++) {
  element = links[i];
  element.addEventListener("click", function (e) {
    e.preventDefault();
    form.setAttribute("action", this.getAttribute("href"));
    form.submit();
  });
}
