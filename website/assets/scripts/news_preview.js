import 'jquery';

$(document).ready(function ($) {
    $('input[name="_addanother"]')
        .before('<input type="button" value="Preview" id="preview" />');

    $('#preview')
        .on('click', () => {
            $('.preview').remove();

            const textArea = $('textarea[name="content"]');
            const newElem = document.createElement("div");
            newElem.classList = "news-content preview";

            textArea.after(newElem);

            newElem.innerHTML = textArea.val();
        });
});
