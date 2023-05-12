function backgroundAnimation() {
  const colors = ['#e3d3ba', '#A67C5B', '#DFC8B4', '#ac8a64', '#c9b18c', '#d8c2a3']; // earth tones colors
  let colorIndex = 0;
  let intervalId;

  function changeColor() {
    const body = document.querySelector("body");
    body.style.transition = "background-color 2s ease";
    body.style.backgroundColor = colors[colorIndex];
    colorIndex = (colorIndex + 1) % colors.length;
  }

  return {
    start() {
      intervalId = setInterval(changeColor, 5000);
    },
    stop() {
      clearInterval(intervalId);
    }
  };
}

const animation = backgroundAnimation();
animation.start();
