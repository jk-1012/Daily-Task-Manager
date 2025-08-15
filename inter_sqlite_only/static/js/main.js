// static/js/main.js
(function(){
    // Get Django CSRF token from cookie
    window.getCSRFToken = function(){
      let cookieValue = null;
      const cookies = document.cookie ? document.cookie.split(';') : [];
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, 10) === 'csrftoken=') {
          cookieValue = decodeURIComponent(cookie.substring(10));
          break;
        }
      }
      return cookieValue;
    };
  
    // Logout helper: POST to /logout/, then go to /login/
    window.logout = function(){
      fetch('/logout/', { method: 'POST', headers: { 'X-CSRFToken': getCSRFToken() } })
        .then(() => window.location.href = '/login/');
    };
  })();
  