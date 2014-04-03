
// var EntityTypes = {
//     'health_region': "RÉGIONS",
//     'health_district': "DISTRICTS",
//     'health_center': "UNITÉS SANITAIRES",
//     'vfq': "VILLAGES",
// };

// var health_entities_types = ['health_region', 'health_district', 'health_center', 'vfq'];
// var health_entities_names = [];

// function getNextEntityTypeLevel(current_level) {
//     var idx = health_entities_types.indexOf(current_level);
//     try {
//         return health_entities_types[idx + 1];
//     } catch (e) {
//         return null;
//     }
// }

// function resetFilterSelect(selectElem) {
//     selectElem.empty();
//     var option = $('<option value="-1" />');
//     option.text(":: " + EntityTypes[getEntityTypeFromSelect(selectElem)]);
//     selectElem.append(option);
// }

// function getEntityTypeFromSelect(selectElem) {
//     return selectElem.attr('id').replace('filter_', '');
// }

// function registerEntityFilter(launch) {
//     console.log("registerEntityFilter");

//     $("#entity_filter select, #report_entity_filter select[id!='filter_period']").on('change', function (e) {
//         console.log($(this).attr('id'));
//         var selected = $(this).val();
//         console.log(selected);
//         var next_level = getNextEntityTypeLevel(getEntityTypeFromSelect($(this)));
//         console.log(next_level);
//         if (next_level != null) {
//             requestEntitiesForFilter(selected, next_level);
//         }
//     });

//     if (launch === true) {
//         requestEntitiesForFilter(null, 'health_region');
//     }

// }

// function requestEntitiesForFilter(parent_slug, type_slug) {
//     if (parent_slug == null || parent_slug == undefined)
//         parent_slug = '___';

//     if (type_slug == null || type_slug == undefined)
//         type_slug = '__all__';

//     function getTarget(entity) {
//         if (entity.type == 'region')
//             return filter_region;
//     }

//     $.get("/api/entities/getchildren/" + parent_slug + "/" + type_slug)
//         .success(function (data) {
//             var target_select = $('#filter_' + type_slug);
//             resetFilterSelect(target_select);
//             var next_level = getNextEntityTypeLevel(type_slug);
//             requestEntitiesForFilter(null, next_level);
//             if (data[0] === undefined) {
//                 return;
//             }
//             $.each(data, function (index, entity) {
//                 var option = $('<option />');
//                 option.val(entity.slug);
//                 option.text(entity.name);
//                 target_select.append(option);
//             });

//     });
// }

// function getNextLevelFor(level, lineage) {
//     var index = lineage.indexOf(level);
//     // don't do anything if at last level
//     if (index == lineage.length - 1) {
//         return null;
//     }
//     return lineage[index + 1];
// }


// function getSelectedFor(level, lineage_data) {
//     var index = lineage_data.indexOf(level);
//     // don't do anything if at last level
//     if (index == lineage_data.length - 1) {
//         return null;
//     }
//     return lineage_data[index + 1];
// }


function getEntitiesBrowser (options) {

    function EntitiesBrowser (options) {

        console.log("Creating EntitiesBrowser");

        this.parentID = options.parentID || null;
        this.baseURL = options.baseURL || "/api/entities/getchildren";
        this.lineage = options.lineage || ['country', 'health_region'];
        this.auto_launch = options.auto_launch || false;
        this.lineage_data = options.lineage_data || [];
        this.add_default_option = (!options.add_default_option) ? false : true;
        this.default_option_data = options.default_option_data || {value: '-1', label: "Tous"};
        this.root = options.root || null;

        // can't do shit without a parentID
        if (this.parentID === null) {
            return;
        }

        this.parentElem = $('#' + this.parentID);

        console.log("lineage_data");
        console.log(this.lineage_data);

        // register action on change for selects
        this.registerOnChange();

        // if we need to populate first
        if (this.populate_first) {

        }

        // launch
        if (this.auto_launch) {
            var first_level = this.lineage[0];
            var first_select = this.getSelectFor(first_level);
            console.log(first_select);
            var selected_value = this.selectedValueFor(first_level);
            console.log("marking " + first_level + " select with " + selected_value);
            this.setSelectedOn(first_select, selected_value);
            first_select.change();
        }

    }

    EntitiesBrowser.prototype.getEntitySlug = function () {
        for (var i=this.lineage.length - 1; i >= 0 ; i--) {
            var entity = this.getSelectFor(this.lineage[i]).val();
            if (entity && entity != this.default_option_data.value) {
                return entity;
            }
        }
        return this.root;
    };

    EntitiesBrowser.prototype.setSelectedOn = function (selectElem, selected_value) {
        selectElem.children("option[value="+ selected_value +"]").attr('selected', 'selected');
        return selectElem;
    };

    EntitiesBrowser.prototype.getIndexFor = function (type_slug) {
        return this.lineage.indexOf(type_slug);
    };

    EntitiesBrowser.prototype.selectedValueFor = function (type_slug) {
        try {
            return this.lineage_data[this.getIndexFor(type_slug)];
        } catch (e) {
            return null;
        }
    };

    EntitiesBrowser.prototype.getNextLevelFrom = function (type_slug) {
        try {
            return this.lineage[this.getIndexFor(type_slug) + 1];
        } catch (e) {
            return null;
        }
    };

    EntitiesBrowser.prototype.clearSelect = function (selectElem) {
        selectElem.empty();
        if (this.add_default_option) {
            var option = $('<option />');
            option.val(this.default_option_data.value);
            option.text(this.default_option_data.label);
            selectElem.append(option);
        }
        return selectElem;
    };

    EntitiesBrowser.prototype.getSelectFor = function(type_slug) {
        return this.parentElem.find('select.entity_filter[data-level="'+ type_slug +'"]');
    };

    EntitiesBrowser.prototype.registerOnChange = function() {
        var manager = this;
        this.parentElem.find('select.entity_filter').on('change', function (e) {
            e.preventDefault();

            // get selected value. this will be new parent.
            var selected = $(this).val();
            if (selected == manager.default_option_data.value) {
                selected = null;
            }

            var type_slug = $(this).data('level');

            var next_type_slug = manager.getNextLevelFrom(type_slug);
            if (!next_type_slug) {
                return;
            }

            if (selected === null) {
                // we selected an empty one. let's propagate.
                var selectElem = manager.clearSelect(manager.getSelectFor(next_type_slug));
                selectElem.change();
                return;
            }

            // fetch data for next level in lineage and parent = selected
            $.get(manager.baseURL + "/" + selected + "/" + next_type_slug)
                .success(function (data) {

                    // grab and reset the select for new slug
                    var selectElem = manager.clearSelect(manager.getSelectFor(next_type_slug));

                    // exit if no data
                    if (data[0] === undefined) {
                        return;
                    }

                    // populate with fetched data
                    $.each(data, function (index, entity) {
                        var option = $('<option />');
                        option.val(entity.slug);
                        option.text(entity.name);
                        selectElem.append(option);
                    });

                    // mark selected if exists
                    var selected_value = manager.selectedValueFor(next_type_slug);
                    if (selected_value !== null) {
                        manager.setSelectedOn(selectElem, selected_value);
                        // selectElem.children("option[value="+ selected_value +"]").attr('selected', 'selected');
                        selectElem.change();
                    }
            });
        });
        console.log("registered onChange");
    };

    return new EntitiesBrowser(options);
}

