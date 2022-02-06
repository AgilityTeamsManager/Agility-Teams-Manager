$(document).ready(function () {
   $(this).bind("contextmenu", function (event) {
     // event.preventDefault();
   });

   createLink();

   $("body").append('<div id="overlay"><i class="fas fa-paw"></i></div>');
   $("#overlay").hide();

   $("a").not('.nooverlay').click(function () {
      target = $(this).attr("target");
      if (target != "_blank") {
         $("#overlay").show();
         console.log("overlay");
      }
   });

  // $('[data-toggle="tooltip"]').tooltip();

   $("body").on("click", ".tuile", function () {
      $("#overlay").show();
      $(this).find("form").submit();
      var f = $(this).find("form");
      if (f) f.submit();
   });

   var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
   
   var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
      return new bootstrap.Tooltip(popoverTriggerEl,{
         boundary: document.body});
   });
   console.log(popoverList);

   $("#bmenuprincipal").click(function (ev) {
      var left = $("#wrapper").position().left;
      console.log(left);
      if (left == 0) {
         OpenLeftMenu();
      } else {
         CloseLeftMenu();
      }
      ev.stopPropagation();
   });

   $("#buser").click(function (ev) {
      console.log("buser");
      window.location = "mon_espace_cneac.php";
   });

   $("#wrapper").click(function () {
      if ($(window).width() < 991) CloseLeftMenu();
   });

   var forms = document.getElementsByClassName("needs-validation");
   // Loop over them and prevent submission
   var validation = Array.prototype.filter.call(forms, function (form) {
      form.addEventListener(
         "submit",
         function (event) {
            if (form.checkValidity() === false) {
               event.preventDefault();
               event.stopPropagation();
            }
            form.classList.add("was-validated");
         },
         false
      );
   });

   $(window).resize(function () {
      if ($(window).width() < 991) CloseLeftMenu();
      else {
         var pl = $("#wrapper").css("padding-left");
         if (parseFloat(pl) > 0) $("#menu_gauche").show();
      }
      equal_cols(".tuile");
   });
   equal_cols(".tuile");
   var prevScrollpos = window.pageYOffset;

   $(window).scroll(function () {
      if ($(window).width() > 991) return;
      var currentScrollPos = window.pageYOffset;
      if (Math.abs(prevScrollpos - currentScrollPos) > 10 || currentScrollPos < 80) {
         if (prevScrollpos > currentScrollPos || currentScrollPos < 80) {
            $(".menu-mobile").css({ top: "0" });
            $("#breadcrumps").css({ top: "60px" });
         } else {
            $(".menu-mobile").css({ top: "-60px" });
            $("#breadcrumps").css({ top: "-200px" });
         }
      }
      prevScrollpos = currentScrollPos;

      if (currentScrollPos < 0) {
         //  $(window).scrollTop( 0 );
         //  prevScrollpos = currentScrollPos = 0;
      }
   });
});

function OpenLeftMenu() {
   //$("#wrapper").css({ left: "250px" });
   $("#menu_gauche").show();
   $("#wrapper,.menu-mobile,#breadcrumps").animate(
      {
         left: "250",
      },
      300,
      "swing",
      function () {}
   );

   //  $('.menu-mobile').css({ left: "250px" });
}

function CloseLeftMenu() {
   $("#wrapper,.menu-mobile,#breadcrumps").animate(
      {
         left: "0",
      },
      300,
      "swing",
      function () {
         $("#menu_gauche").hide();
         console.log("menu caché");
      }
   );
}

function equal_cols(el) {
   var h = 0;
   $(el).each(function () {
      $(this).css({ height: "auto" });
      if ($(this).outerHeight() > h) {
         h = $(this).outerHeight();
      }
   });

   $(el).each(function () {
      $(this).css({ height: h });
   });
}

function createLink() {
   $(".lienbleu2").each(function (index) {
      var a = $("<span />").text($(this).text());
      var i = $("<i />").addClass("ms-2 fa fa-angle-double-right");
      $(this).text("");
      a.appendTo($(this));
      i.appendTo($(this));
   });
}
