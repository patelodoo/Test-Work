/** @odoo-module **/
import { onWillStart } from "@odoo/owl";
import { patch } from "@web/core/utils/patch";
import PublicKiosk from "@hr_attendance/public_kiosk/public_kiosk_app";


patch(PublicKiosk.kioskAttendanceApp.prototype, {

    setup() {
        super.setup();
        this.state.project = false;
        this.state.task = false;
        this.state.description = false;
        this.state.tasks = [];
        this.state.projectMandatoryError = false;
        this.state.taskMandatoryError = false;
        this.state.descMandatoryError = false;
        onWillStart(async () => {
            var project_data = await this.rpc('projects_data', {
                'token': this.props.token,
            })
            this.props.projects = project_data['projects'];
            this.props.tasks = project_data['tasks'];
        });
    },

    onProjectChanged(ev){
        var projectId = ev.target.value;
        if(projectId){
            this.state.project = projectId
            this.state.projectMandatoryError = false;
            var tasks = this.props.tasks.filter((r) => r.project_id && r.project_id == parseInt(projectId))
            this.state.tasks = tasks;
        }else{
            this.state.project = false
            this.state.projectMandatoryError = false;
            this.state.task = false
        }
    },

    onTaskChanged(ev){
        var taskId = ev.target.value;
        if(taskId){
            this.state.task = taskId
            this.state.taskMandatoryError = false;
        }else{
            this.state.task = false
        }
    },

    onDescriptionChanged(ev){
        var description = ev.target.value;
        console.log("Description=", description)
        if(description && description.length > 0){
            this.state.description = description
            this.state.descMandatoryError = false;
        }else{
            this.state.description = false
        }
    },

    async kioskConfirm(employeeId){
        var canProcess = true
        if(!this.state.project){
            this.state.projectMandatoryError = true
            canProcess = false
        }
        if(!this.state.task){
            this.state.taskMandatoryError = true
            canProcess = false
        }
        if(!this.state.description || this.state.description.length == 0){
            this.state.descMandatoryError = true
            canProcess = false
        }
        if(canProcess){
            await super.kioskConfirm(...arguments);
            if(this.state.active_display == 'greet'){
                this.state.project = false;
                this.state.task = false;
            }
        }
    },

    async onManualSelection(employeeId, enteredPin){
        var canProcess = true
        if(!this.state.project){
            this.state.projectMandatoryError = true
            canProcess = false
        }
        if(!this.state.task){
            this.state.taskMandatoryError = true
            canProcess = false
        }
        if(!this.state.description || this.state.description.length == 0){
            this.state.descMandatoryError = true
            canProcess = false
        }
        if(canProcess){
            await super.onManualSelection(...arguments);
            await this.rpc('update_project_data',
            {
                'update_data': {'project_id': parseInt(this.state.project), 'task_id': parseInt(this.state.task), 'attendance_description': this.state.description},
                'attendance_id': this.employeeData.last_attendance_id,
            })
            if(this.state.active_display == 'greet'){
                this.state.project = false;
                this.state.task = false;
                this.state.description = false;
            }
        }
    },

    async onBarcodeScanned(barcode){
        var canProcess = true
        if(!this.state.project){
            this.state.projectMandatoryError = true
            canProcess = false
        }
        if(!this.state.task){
            this.state.taskMandatoryError = true
            canProcess = false
        }
        if(!this.state.description || this.state.description.length == 0){
            this.state.descMandatoryError = true
            canProcess = false
        }
        if(canProcess){
            await super.onBarcodeScanned(...arguments);
            await this.rpc('update_project_data',
            {
                'update_data': {'project_id': parseInt(this.state.project), 'task_id': parseInt(this.state.task), 'attendance_description': this.state.description},
                'attendance_id': this.employeeData.last_attendance_id,
            })
            if(this.state.active_display == 'greet'){
                this.state.project = false;
                this.state.task = false;
                this.state.description = false;
            }
        }
    },
});