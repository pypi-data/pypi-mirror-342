function toggleOtherServiceDescription(checkbox) {
    const descriptionField = document.getElementById('other_service_description');
    if (checkbox.checked) {
        descriptionField.style.display = 'block';  // Показываем поле
    } else {
        descriptionField.style.display = 'none';  // Скрываем поле
    }
}

document.addEventListener("DOMContentLoaded", function() {
    const mainContent = document.querySelector('main');
    mainContent.style.opacity = 0;
    setTimeout(() => {
        mainContent.style.transition = "opacity 0.5s";
        mainContent.style.opacity = 1;
    }, 100);
});

document.addEventListener('DOMContentLoaded', function() {
    const phoneInput = document.querySelector('input[data-mask]');
    if (phoneInput) {
        phoneInput.addEventListener('input', function(e) {
            const value = e.target.value.replace(/\D/g, ''); // Удаляем все нецифровые символы
            let formattedValue = '+7(';

            if (value.length > 1) {
                formattedValue += value.slice(1, 4); // Добавляем первые 3 цифры
            }
            if (value.length >= 4) {
                formattedValue += ')-';
                formattedValue += value.slice(4, 7); // Добавляем следующие 3 цифры
            }
            if (value.length >= 7) {
                formattedValue += '-';
                formattedValue += value.slice(7, 9); // Добавляем следующие 2 цифры
            }
            if (value.length >= 9) {
                formattedValue += '-';
                formattedValue += value.slice(9, 11); // Добавляем последние 2 цифры
            }

            e.target.value = formattedValue;
        });

        // Обработка удаления символов
        phoneInput.addEventListener('keydown', function(e) {
            if (e.key === 'Backspace' || e.key === 'Delete') {
                const value = e.target.value.replace(/\D/g, ''); // Удаляем все нецифровые символы
                let cursorPosition = e.target.selectionStart; // Позиция курсора

                // Если пользователь пытается удалить символ маски (например, скобку или тире),
                // перемещаем курсор на одну позицию назад
                if (e.target.value[cursorPosition - 1] === '(' || 
                    e.target.value[cursorPosition - 1] === ')' || 
                    e.target.value[cursorPosition - 1] === '-') {
                    e.preventDefault(); // Отменяем стандартное поведение
                    e.target.setSelectionRange(cursorPosition - 1, cursorPosition - 1); // Перемещаем курсор
                }
            }
        });
    }
});

function toggleServiceFields(checkbox) {
    const serviceField = document.getElementById('service_field');
    const otherServiceDescription = document.getElementById('other_service_description');

    if (checkbox.checked) {
        serviceField.style.display = 'none';
        otherServiceDescription.style.display = 'block';
    } else {
        serviceField.style.display = 'block';
        otherServiceDescription.style.display = 'none';
    }
}

