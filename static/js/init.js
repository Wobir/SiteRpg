// Add Bootstrap classes to inputs/buttons when templates don't include them
document.addEventListener('DOMContentLoaded', function () {
  try {
    document.querySelectorAll('input:not([type=hidden]):not(.form-control), textarea:not(.form-control), select:not(.form-control)').forEach(function(el){
      el.classList.add('form-control');
    });
    document.querySelectorAll('button:not(.btn), input[type=submit]:not(.btn)').forEach(function(btn){
      btn.classList.add('btn','btn-primary');
    });
  } catch (e) {
    // silent
    console.error(e);
  }
});
