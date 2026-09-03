(function() {
    'use strict';

    function ready(fn) {
        if (document.readyState !== 'loading') {
            fn();
        } else {
            document.addEventListener('DOMContentLoaded', fn);
        }
    }

    ready(function () {
        var attributeSelect = document.getElementById('id_attribute_filter');
        var valuesSelect = document.getElementById('id_values_picker');
        var finalSelect = document.getElementById('id_attributes_final');

        if (!attributeSelect || !valuesSelect || !finalSelect) {
            return; // Fields not present on this page
        }

        // Build the "Add selected" / "Remove selected" buttons dynamically
        var addBtn = document.createElement('button');
        addBtn.type = 'button';
        addBtn.textContent = 'Add selected ▸';
        addBtn.style.margin = '5px 0';
        valuesSelect.parentNode.insertBefore(addBtn, valuesSelect.nextSibling);

        var removeBtn = document.createElement('button');
        removeBtn.type = 'button';
        removeBtn.textContent = '◂ Remove selected';
        removeBtn.style.margin = '5px 0';
        finalSelect.parentNode.insertBefore(removeBtn, finalSelect.nextSibling);

        // Fetch the admin base URL (works regardless of admin URL prefix)
        var ajaxUrl = attributeSelect.dataset.ajaxUrl ||
            (window.location.pathname.split('/product/')[0] + '/product/ajax/values-by-attribute/');

        function loadValuesForAttribute(attributeId) {
            valuesSelect.innerHTML = '';
            if (!attributeId) {
                return;
            }

            var url = ajaxUrl + '?attribute_id=' + encodeURIComponent(attributeId);

            fetch(url, {
                headers: {'X-Requested-With': 'XMLHttpRequest'},
                credentials: 'same-origin',
            })
                .then(function (resp) {
                    if (!resp.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return resp.json();
                })
                .then(function (data) {
                    var existingIds = getFinalIds();
                    data.results.forEach(function (item) {
                        // Don't show values already added to the final list
                        if (existingIds.indexOf(String(item.id)) !== -1) {
                            return;
                        }
                        var opt = document.createElement('option');
                        opt.value = item.id;
                        opt.textContent = item.text;
                        valuesSelect.appendChild(opt);
                    });
                })
                .catch(function (err) {
                    console.error('Failed to load attribute values:', err);
                });
        }

        function getFinalIds() {
            return Array.prototype.map.call(finalSelect.options, function (o) {
                return o.value;
            });
        }

        function addSelectedValues() {
            var selectedOptions = Array.prototype.filter.call(
                valuesSelect.options, function (o) { return o.selected; }
            );

            selectedOptions.forEach(function (o) {
                // Avoid duplicates
                var already = getFinalIds().indexOf(o.value) !== -1;
                if (!already) {
                    var newOpt = document.createElement('option');
                    newOpt.value = o.value;
                    newOpt.textContent = o.textContent;
                    newOpt.selected = true; // must be selected to be submitted
                    finalSelect.appendChild(newOpt);
                }
                o.remove();
            });
        }

        function removeSelectedValues() {
            var selectedOptions = Array.prototype.filter.call(
                finalSelect.options, function (o) { return o.selected; }
            );
            selectedOptions.forEach(function (o) { o.remove(); });
        }

        // Ensure ALL options in the final select are marked selected right
        // before submit, since only selected <option>s get posted.
        var formEl = finalSelect.closest('form');
        if (formEl) {
            formEl.addEventListener('submit', function () {
                Array.prototype.forEach.call(finalSelect.options, function (o) {
                    o.selected = true;
                });
            });
        }

        attributeSelect.addEventListener('change', function () {
            loadValuesForAttribute(this.value);
        });

        addBtn.addEventListener('click', addSelectedValues);
        removeBtn.addEventListener('click', removeSelectedValues);

        // If attribute already selected on page load (e.g. validation error), populate values
        if (attributeSelect.value) {
            loadValuesForAttribute(attributeSelect.value);
        }
    });
})();