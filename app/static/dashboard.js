$(document).ready(function() {
    // Click event for downloading CSV report
    $('#download-csv').click(function() {
        const filters = {
            state: $('#state').val(),
            district: $('#district').val(),
            tb_incidence: $('#tb_incidence').val(),
            diabetes: $('#diabetes').val(),
            malaria_incidence: $('#malaria_incidence').val(),
            hiv_aids: $('#hiv_aids').val(),
            imr: $('#imr').val(),
            vaccination: $('#vaccination').val(),
            income: $('#income').val(),
            employment_rate: $('#employment_rate').val(),
            education: $('#education').val(),
            housing: $('#housing').val(),
            urbanization: $('#urbanization').val(),
            aqi: $('#aqi').val(),
            annual_rainfall: $('#annual_rainfall').val(),
            healthcare_access: $('#healthcare_access').val(),
        };

        const queryString = $.param(filters);
        window.location.href = `/download-report?${queryString}`;
    });

    // Click event for downloading PDF report
    $('#download-pdf').click(function() {
        const filters = {
            state: $('#state').val(),
            district: $('#district').val(),
            tb_incidence: $('#tb_incidence').val(),
            diabetes: $('#diabetes').val(),
            malaria_incidence: $('#malaria_incidence').val(),
            hiv_aids: $('#hiv_aids').val(),
            imr: $('#imr').val(),
            vaccination: $('#vaccination').val(),
            income: $('#income').val(),
            employment_rate: $('#employment_rate').val(),
            education: $('#education').val(),
            housing: $('#housing').val(),
            urbanization: $('#urbanization').val(),
            aqi: $('#aqi').val(),
            annual_rainfall: $('#annual_rainfall').val(),
            healthcare_access: $('#healthcare_access').val(),
        };

        const queryString = $.param(filters);
        window.location.href = `/download-report/pdf?${queryString}`;
    });

    // Chart rendering function
    function renderHealthChart(data) {
        var ctx = document.getElementById('healthChart').getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: [
                    'TB Incidence', 
                    'Diabetes', 
                    'Malaria Incidence', 
                    'HIV/AIDS', 
                    'IMR', 
                    'Vaccination', 
                    'Income (INR)', 
                    'Employment Rate', 
                    'Education', 
                    'Housing', 
                    'Urbanization', 
                    'AQI', 
                    'Annual Rainfall (mm)', 
                    'Healthcare Access'
                ],
                datasets: [{
                    label: 'Health Metrics',
                    data: [
                        data.tb_incidence, 
                        data.diabetes, 
                        data.malaria_incidence, 
                        data.hiv_aids, 
                        data.imr, 
                        data.vaccination, 
                        data.income, 
                        data.employment_rate, 
                        data.education, 
                        data.housing, 
                        data.urbanization, 
                        data.aqi, 
                        data.annual_rainfall, 
                        data.healthcare_access
                    ],
                    backgroundColor: [
                        '#4CAF50', '#FFC107', '#F44336', '#2196F3', '#9C27B0', 
                        '#FF9800', '#FF5722', '#795548', '#607D8B', '#3F51B5', 
                        '#009688', '#8BC34A', '#CDDC39', '#FFEB3B'
                    ]
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }

    // Function to fetch and filter health data
    function filterHealthData() {
        const filters = {
            state: $('#state').val(),
            district: $('#district').val(),
            tb_incidence: $('#tb_incidence').val(),
            diabetes: $('#diabetes').val(),
            malaria_incidence: $('#malaria_incidence').val(),
            hiv_aids: $('#hiv_aids').val(),
            imr: $('#imr').val(),
            vaccination: $('#vaccination').val(),
            income: $('#income').val(),
            employment_rate: $('#employment_rate').val(),
            education: $('#education').val(),
            housing: $('#housing').val(),
            urbanization: $('#urbanization').val(),
            aqi: $('#aqi').val(),
            annual_rainfall: $('#annual_rainfall').val(),
            healthcare_access: $('#healthcare_access').val(),
        };

        $.post('/filter-health-data', filters, function(response) {
            renderHealthChart(response);
        }).fail(function(error) {
            console.error('Error fetching health data:', error);
        });
    }

    // Initialize the map
    var map = L.map('map').setView([20.5937, 78.9629], 5);  // Set initial view to India

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 18
    }).addTo(map);

    // Function to add markers for healthcare access
    function renderMapMarkers(data) {
        data.forEach(function(location) {
            var color;
            if (location.healthcare_access <= 1) {
                color = 'red';
            } else if (location.healthcare_access <= 3) {
                color = 'yellow';
            } else {
                color = 'green';
            }

            L.circleMarker([location.latitude, location.longitude], {
                color: color,
                radius: 8
            }).addTo(map).bindPopup(`District: ${location.district}<br>Healthcare Access: ${location.healthcare_access}`);
        });
    }

    // Function to fetch and filter map data
    function filterMapData() {
        const filters = {
            state: $('#state').val(),
            district: $('#district').val()
        };

        $.post('/filter-map-data', filters, function(response) {
            renderMapMarkers(response.data);
        }).fail(function(error) {
            console.error('Error fetching map data:', error);
        });
    }

    // Initialize data filtering when the page loads
    filterHealthData();
    filterMapData();

    // Optionally, you can bind the filtering functions to filter form submissions
    $('#filterForm').on('submit', function(e) {
        e.preventDefault();  
        filterHealthData();  
        filterMapData();     
    });
});
