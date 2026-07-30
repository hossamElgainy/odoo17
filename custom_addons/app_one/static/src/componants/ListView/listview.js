/*@odoo-module*/
import {Component, useState, onWillUnmount} from "@odoo/owl";
import {registry} from "@web/core/registry";
import {useService} from "@web/core/utils/hooks";

export class ListViewAction extends Component {
    static template = "app_one.ListView";

    setup() {
        this.state = useState({
            "records": []
        });
        this.orm = useService('orm');
        this.rpc = useService('rpc');
        this.loadRecords();

        this.intervalUpdate = setInterval(() => this.loadRecords(), 3000);
        onWillUnmount(() => {
            clearInterval(this.intervalUpdate)
        });
    }

    // async loadRecords(){
    //     const result = await this.orm.searchRead("property",[],[]);
    //     console.log(result)
    //     this.state.records = result;
    // }
    async loadRecords() {
        const result = await this.rpc("/web/dataset/call_kw", {
            model: "property",
            method: "search_read",
            args: [[]], // domain
            kwargs: {fields: ["id", "name", "postcode", "date_availability", "selling_price", "state", "owner_id"]}
        });
        console.log(result)
        this.state.records = result;
    }
    async createRecord(){
        await this.rpc("/web/dataset/call_kw",{
            model:"property",
            method:"create",
            args:[{
                name:"Created Form The Component",
                postcode:"21197",
                date_availability:"2026-07-19"
            }],
            kwargs:{}
        })
        this.loadRecords();
    }
    async deleteRecord(recordId){
        await this.rpc("/web/dataset/call_kw",{
            model:"property",
            method:"unlink",
            args:[recordId],
            kwargs:{}
        })
        this.loadRecords();
    }
}

registry.category("actions").add("app_one.action_list_view", ListViewAction);