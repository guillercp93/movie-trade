function autocomplete(data) {
    console.log(data);
    var options = {
        url: data,
    
        getValue: "name",
    
        template: {
            type: "description",
            fields: {
                description: "email"
            }
        },
    
        list: {
            match: {
                enabled: true
            }
        },
    
        theme: "plate-dark"
    };
    
    $("#data_movies").easyAutocomplete(options);
}