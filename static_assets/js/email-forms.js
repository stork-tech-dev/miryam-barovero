(function () {
  var config = window.MIRYAM_EMAILJS;
  if (!config || !config.publicKey) return;

  if (typeof emailjs === "undefined") {
    console.error("EmailJS SDK no cargado");
    return;
  }

  emailjs.init(config.publicKey);

  function isConfigured() {
    return (
      config.serviceId &&
      config.templateId &&
      config.publicKey &&
      config.serviceId.indexOf("YOUR_") !== 0
    );
  }

  function showSiteToast(title, text, isError, options) {
    options = options || {};
    var existing = document.getElementById("siteToastOverlay");
    if (existing) existing.remove();

    var overlay = document.createElement("div");
    overlay.id = "siteToastOverlay";
    overlay.className = "site-toast-overlay is-visible";
    overlay.setAttribute("aria-live", "polite");
    if (options.redirectOnClose) {
      overlay.setAttribute("data-redirect-on-close", options.redirectOnClose);
    }

    var toast = document.createElement("div");
    toast.className = "site-toast site-toast--" + (isError ? "error" : "success");
    toast.setAttribute("role", "alert");

    var titleEl = document.createElement("p");
    titleEl.className = "site-toast__title";
    titleEl.textContent = title;

    var textEl = document.createElement("p");
    textEl.className = "site-toast__text";
    textEl.textContent = text;

    var closeBtn = document.createElement("button");
    closeBtn.type = "button";
    closeBtn.className = "site-toast__close";
    closeBtn.setAttribute("data-dismiss", "toast");
    closeBtn.setAttribute("aria-label", "Cerrar mensaje");
    closeBtn.innerHTML = "<span aria-hidden=\"true\">&times;</span>";

    toast.appendChild(titleEl);
    toast.appendChild(textEl);
    toast.appendChild(closeBtn);
    overlay.appendChild(toast);
    document.body.appendChild(overlay);

    if (typeof window.initSiteToast === "function") {
      window.initSiteToast();
    } else {
      function dismissWithRedirect() {
        var redirectUrl = overlay.getAttribute("data-redirect-on-close");
        overlay.remove();
        if (redirectUrl) {
          window.location.href = redirectUrl;
        }
      }
      closeBtn.addEventListener("click", dismissWithRedirect);
      overlay.addEventListener("click", function (event) {
        if (event.target === overlay || event.target.closest("[data-dismiss='toast']")) {
          dismissWithRedirect();
        }
      });
    }
  }

  function normalizeEmail(value) {
    return (value || "").trim();
  }

  function buildTemplateParams(templateParams) {
    var fromEmail = normalizeEmail(templateParams.from_email);
    var fromName = (templateParams.from_name || "").trim();
    var company = templateParams.company || "";
    var message = templateParams.message || "";
    var toEmail = templateParams.to_email || config.toEmail || "";

    /* Nombre visible + mail del formulario como emisor / reply */
    var senderName = fromName;
    if (fromEmail) {
      senderName = fromName ? fromName + " (" + fromEmail + ")" : fromEmail;
    }

    return {
      from_name: senderName,
      from_email: fromEmail,
      reply_to: fromEmail,
      company: company,
      message: message,
      to_email: toEmail,
      /* Alias para plantillas EmailJS */
      name: fromName || fromEmail,
      nombre: fromName || fromEmail,
      email: fromEmail,
      user_email: fromEmail,
      title: company,
      mensaje: message,
      time: new Date().toLocaleString("es-AR", {
        dateStyle: "short",
        timeStyle: "short",
      }),
    };
  }

  function sendEmail(templateParams) {
    if (!isConfigured()) {
      return Promise.reject(new Error("EmailJS no configurado"));
    }
    return emailjs.send(
      config.serviceId,
      config.templateId,
      buildTemplateParams(templateParams)
    );
  }

  function emailjsErrorMessage(err) {
    if (err && err.text) return err.text;
    if (err && err.message) return err.message;
    return "Error desconocido";
  }

  function bindFullTestRequest() {
    document.querySelectorAll(".js-emailjs-full-test").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var nombre = (btn.getAttribute("data-nombre") || "").trim();
        var email = (btn.getAttribute("data-email") || "").trim();
        var tipo = btn.getAttribute("data-tipo") || "";
        var tipoNombre = btn.getAttribute("data-tipo-nombre") || "";

        if (!email) {
          showSiteToast(
            "No se pudo enviar",
            "Completá tu email en el test para que podamos contactarte.",
            true
          );
          return;
        }

        var fromName = nombre || "Participante test Eneagrama";
        var fromEmail = email;
        var message = "ENVIAME EL TEST COMPLETO";

        if (tipo && tipoNombre) {
          message +=
            "\n\nResultado del test rápido: Tipo " +
            tipo +
            " — " +
            tipoNombre;
        }
        if (nombre) {
          message += "\nNombre: " + nombre;
        }

        var originalText = btn.textContent;
        btn.disabled = true;
        btn.textContent = "Enviando...";

        sendEmail({
          from_name: fromName,
          from_email: fromEmail,
          company: "Miryam Barovero — Solicitud test completo",
          message: message,
          to_email: config.toEmail,
        })
          .then(function () {
            showSiteToast(
              "¡Mensaje enviado!",
              "Recibimos tu solicitud del test completo. Te contactaremos a la brevedad.",
              false,
              { redirectOnClose: config.homeUrl || "/" }
            );
          })
          .catch(function (err) {
            console.error("EmailJS test completo:", err, emailjsErrorMessage(err));
            showSiteToast(
              "No se pudo enviar",
              "Hubo un error al enviar la solicitud. Intentá de nuevo o escribinos por WhatsApp.",
              true
            );
          })
          .finally(function () {
            btn.disabled = false;
            btn.textContent = originalText;
          });
      });
    });
  }

  function bindContactForms() {
    document.querySelectorAll(".js-emailjs-contact").forEach(function (form) {
      form.addEventListener("submit", function (event) {
        event.preventDefault();

        var nombre = (form.querySelector("[name=nombre]") || {}).value || "";
        var apellido = (form.querySelector("[name=apellido]") || {}).value || "";
        var email = (form.querySelector("[name=email]") || {}).value || "";
        var consulta = (form.querySelector("[name=consulta]") || {}).value || "";

        nombre = nombre.trim();
        apellido = apellido.trim();
        email = email.trim();
        consulta = consulta.trim();

        if (!nombre || !apellido || !email || !consulta) {
          showSiteToast(
            "No se pudo enviar",
            "Por favor completá todos los campos del formulario.",
            true
          );
          return;
        }

        var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
          showSiteToast("No se pudo enviar", "Por favor ingresá un email válido.", true);
          return;
        }

        var submitBtn = form.querySelector('[type="submit"]');
        var originalText = submitBtn ? submitBtn.textContent : "";
        if (submitBtn) {
          submitBtn.disabled = true;
          submitBtn.textContent = "Enviando...";
        }

        sendEmail({
          from_name: nombre + " " + apellido,
          from_email: email,
          company: "Miryam Barovero — Contacto web",
          message: consulta,
          to_email: config.toEmail,
        })
          .then(function () {
            form.reset();
            showSiteToast(
              "¡Mensaje enviado!",
              "Recibimos tu consulta correctamente. Te responderemos a la brevedad.",
              false
            );
          })
          .catch(function (err) {
            console.error("EmailJS:", err, emailjsErrorMessage(err));
            showSiteToast(
              "No se pudo enviar",
              "Hubo un error al enviar. Intentá de nuevo o escribinos por WhatsApp.",
              true
            );
          })
          .finally(function () {
            if (submitBtn) {
              submitBtn.disabled = false;
              submitBtn.textContent = originalText;
            }
          });
      });
    });
  }

  function sendEnneagramEmailIfNeeded() {
    var dataEl = document.getElementById("enneagram-email-payload");
    if (!dataEl) return;

    var payload;
    try {
      payload = JSON.parse(dataEl.textContent);
    } catch (e) {
      console.error("Payload test Eneagrama inválido", e);
      return;
    }

    sendEmail(payload)
      .then(function () {
        showSiteToast(
          "¡Mensaje enviado!",
          "¡Listo! Tu resultado está abajo. También lo recibimos por mail.",
          false
        );
      })
      .catch(function (err) {
        console.error("EmailJS test:", err, emailjsErrorMessage(err));
        showSiteToast(
          "Aviso",
          "Tu resultado está abajo, pero no pudimos enviar el mail. Podés contactarnos por el formulario.",
          true
        );
      });
  }

  bindContactForms();
  bindFullTestRequest();
  sendEnneagramEmailIfNeeded();
})();
