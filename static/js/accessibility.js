$(document).ready(function () {
    // Initialize accessibility settings on page load
    applyAccessibilitySettings();

    // Event listener for accessibility options modal changes
    $('#high-contrast-checkbox').on('change', function () {
        const isChecked = $(this).is(':checked');
        $('html').attr('data-bs-theme', isChecked ? 'dark' : 'light');
        localStorage.setItem('highContrast', isChecked);
        console.log('High contrast mode set to ' + isChecked);
    });

    $('input[name="text-size"]').on('change', function () {
        const selectedSize = $(this).val();
        if (selectedSize === 'larger') {
            $('body').addClass('text-size-larger');
        } else {
            $('body').removeClass('text-size-larger');
        }
        localStorage.setItem('textSize', selectedSize);
        console.log('Text size set to ' + selectedSize);
    });

    // Function to apply accessibility settings on page load
    function applyAccessibilitySettings() {
        // Apply high contrast mode if enabled
        const highContrast = localStorage.getItem('highContrast') === 'true';
        $('#high-contrast-checkbox').prop('checked', highContrast);
        $('html').attr('data-bs-theme', highContrast ? 'dark' : 'light');

        // Apply text size setting
        const textSize = localStorage.getItem('textSize');
        if (textSize === 'larger') {
            $('body').addClass('text-size-larger');
            $('#textSizeLarger').prop('checked', true);
        } else {
            $('body').removeClass('text-size-larger');
            $('#textSizeRegular').prop('checked', true);
        }
    }

    // When the modal is opened, set the current state based on saved preferences
    $('#accessibilityModal').on('show.bs.modal', function () {
        applyAccessibilitySettings();
    });
});
