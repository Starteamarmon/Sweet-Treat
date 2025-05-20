VANTA.FOG({
            el: "#vanta-bg",
            mouseControls: true,
            touchControls: true,
            gyroControls: false,
            minHeight: 200.0,
            minWidth: 200.0,
            highlightColor: 0xffd778,
            midtoneColor: 0xff8d7b,
            lowlightColor: 0xafdeff,
            baseColor: 0xbee0ff,
            blurFactor: 0.9,
            speed: 2.8,
            zoom: 0.9,
        });

        const rangeInput = document.getElementById("customRange3");
        const rangeValue = document.getElementById("rangeValue");
        const hiddenWeightInput = document.querySelector('input[name="weight"]');

        rangeInput.addEventListener("input", () => {
            rangeValue.textContent = rangeInput.value;
            hiddenWeightInput.value = rangeInput.value;
        });

        document.addEventListener("DOMContentLoaded", () => {
            if (hiddenWeightInput && hiddenWeightInput.value) {
                rangeInput.value = hiddenWeightInput.value;
                rangeValue.textContent = hiddenWeightInput.value;
            }
        });