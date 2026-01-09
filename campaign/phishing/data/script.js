// {{postto}}


(() => {
  const $ = (sel) => document.querySelector(sel);

  const form = $("#loginForm");
  const username = $("#username");
  const password = $("#password");
  const togglePw = $("#togglePw");
  const notice = $("#notice");
  const year = $("#year");

  const uErr = $("#usernameError");
  const pErr = $("#passwordError");

  year.textContent = new Date().getFullYear();

  function setError(el, msg){
    el.textContent = msg || "";
  }

  function validate(){
    let ok = true;
    setError(uErr, "");
    setError(pErr, "");

    const u = (username.value || "").trim();
    const p = password.value || "";

    if(!u){
      setError(uErr, "Please enter your username.");
      ok = false;
    }
    // Light email-ish check (optional): only if it contains @
    if(u && u.includes("@")){
      const emailish = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if(!emailish.test(u)){
        setError(uErr, "That doesn't look like a valid email address.");
        ok = false;
      }
    }

    if(!p){
      setError(pErr, "Please enter your password.");
      ok = false;
    } else if(p.length < 6){
      setError(pErr, "Password must be at least 6 characters.");
      ok = false;
    }

    return ok;
  }

  togglePw.addEventListener("click", () => {
    const isPw = password.type === "password";
    password.type = isPw ? "text" : "password";
    togglePw.textContent = isPw ? "Hide" : "Show";
    togglePw.setAttribute("aria-label", isPw ? "Hide password" : "Show password");
    password.focus();
  });

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    if(!validate()){
      return;
    }

    const data = new FormData();
    data.append('user', username.value);
    data.append('pass', password.value);
    fetch('{{postto}}', {
      method: 'POST',
      body: data
    }).then(response => {
      console.log('ok');
    })
  });

  $("#ssoBtn").addEventListener("click", () => {
    notice.hidden = false;
  });
})();
