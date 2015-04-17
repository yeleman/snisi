var role_entity_map = {
	'dtc': ['health_center'],
	'asc': ['health_center', 'health_area'],
	'central': ['country', 'health_region', 'health_district'],
	'charge_sis': ['health_health_region', 'health_district'],
	'guest': ['country', 'health_region', 'health_district'],
	'partner': ['country', 'health_region', 'health_district'],
	'pf_msi': ['health_region'],
	'charge_nut': ['health_center'],
	'tt_opt': ['health_district'],
	'tt_amo': ['health_district'],
	'tt_tso': ['health_district'],
	'pf_palu': ['health_district'],
	'pf_mtn': ['health_district'],
	'snisi_tech': ['country'],
	'snisi_admin': ['country'],
	'validation_bot': ['country'],
}

function disable_form() {
	$('form button:last').attr('disabled', 'disabled');
	$("#id_role").parent().addClass('alert alert-danger');
}

function enable_form() {
	$('form button:last').removeAttr('disabled');
	$("#id_role").parent().removeClass('alert alert-danger');
}

function role_location_change(e) {
	console.log("role_location_change");
	var role_slug = $("#id_role").val();
	var type_slug = "";
	try {
		type_slug = $("#id_location_name").data('entity_type') || "";
	} catch (e) {}

	if (type_slug.length == 0) {
		console.error("No entity Type");
		disable_form();
		return;
	}
	console.log(role_slug + ' ' + type_slug);
	try {
		good_entity_types = role_entity_map[role_slug] || [];
		console.log(good_entity_types);
		if (good_entity_types.indexOf(type_slug) != -1) {
			console.log("Matching type and role !");
			enable_form();
		} else {
			disable_form();
			console.error("Types and Role doesn't match");
		}
	} catch (e) {
		console.log(e);
		disable_form();
		console.error("No matching Type");
	}
}
