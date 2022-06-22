import * as api from "./api.js"


$("#CreateResumeBtn").addEventListener('submit', function(){
    var files = {};
    var resume_content = $(this).value;
    var customer_id = document.getElementById('customer_id').value;
    var response = api.CreateResumeView(customer_id);
    if (!response.status_code in (200, 201)){
            console.log('Exception. Form has not been proceeded.');
        }
    }
});


UpdateBtn.addEventListener('submit', function(){
    var files = {}
    var resume_updated_content = document.getElementById('').value;
    var response = api.UpdateResumeView(customer_id);
    if (!response.status_code in (200, 201)){
        console.log('Exception. Form has not been proceeded.');
    }
});

DeleteBtn.addEventListener('submit', function(){
    var response = api.DeleteResumeView(customer_id);
    if (!response.status_code in (200, 201)){
        console.log('Exception. Form has not been proceeded.');
    }
});
