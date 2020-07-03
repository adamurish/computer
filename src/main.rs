#![feature(proc_macro_hygiene, decl_macro)]

#[macro_use] extern crate rocket;
#[macro_use] extern crate serde_derive;

use rocket::{Rocket, State};
use std::sync::{Arc, Mutex};
use rocket_contrib::json::Json;

//event structs/enums
struct Event {
    id: i32,
    action_id: i32,
}

struct ScheduledEvent {
    trigger_time: i32,
    event: Event,
}

struct List{
    id: i32,
    items: Vec<String>,
}

impl List {
    fn from_csv(id: i32, csv: String) -> List{
        let mut items = Vec::new();
        let iterator = csv.chars();
        let mut string = String::new();

        for c in iterator {
            if c == ',' {
                items.push(string.clone());
                string = String::new();
            }
            string.push(c);
        };

        List {
            id,
            items,
        }
    }
}

struct Reminder{
    id: i32,
    message: String,
}

struct Assistant {
    alarms: Arc<Mutex<Vec<i32>>>,
    lists: Arc<Mutex<Vec<List>>>,
    reminders: Arc<Mutex<Vec<Reminder>>>,
}

struct Automaton {
    scheduled_events: Arc<Mutex<Vec<ScheduledEvent>>>,
}

//JSON templates
#[derive(Serialize, Deserialize)]
enum DataTypes{
    AlarmType,
    ListType,
    ReminderType,
}

#[derive(Deserialize)]
struct AssistantRequest{
    request_type: DataTypes,
    id: i32,
    raw_content: String,
}

#[derive(Serialize)]
struct AssistantResponse{
    response_type: DataTypes,
    content: Vec<String>,
}

impl Assistant {
    fn new() -> Assistant {
        let mut alarm_vec: Vec<i32> = Vec::new();
        let mut list_vec: Vec<List> = Vec::new();
        let mut reminder_vec: Vec<Reminder> = Vec::new();
        Assistant {
            alarms: Arc::new(Mutex::new(alarm_vec)),
            lists: Arc::new(Mutex::new(list_vec)),
            reminders: Arc::new(Mutex::new(reminder_vec)),
        }
    }

    fn add_from_request(&self, request: AssistantRequest) -> Result<(), &str>{
        match request.request_type{
            DataTypes::AlarmType => Ok(self.add_alarm(request.raw_content.parse::<i32>().unwrap())),
            DataTypes::ListType => Ok(self.add_list(List::from_csv(request.id, request.raw_content))),
            DataTypes::ReminderType => Ok(self.add_reminder(Reminder {
                id: request.id,
                message: request.raw_content,
            })),
        }
    }

    fn add_alarm(&self, alarm_time: i32) {
        let mut list = self.alarms.lock().unwrap();
        while list.len() > 3{
            list.pop();
        }
        list.push(alarm_time);
        println!("Added alarm");
    }

    fn add_list(&self, new_list: List) {
        let mut list = self.lists.lock().unwrap();
        list.push(new_list);
        println!("Added list");
    }

    fn add_reminder(&self, reminder: Reminder) {
        let mut list = self.reminders.lock().unwrap();
        list.push(reminder);
        println!("Added reminder");
    }

    fn generate_response(&self, response_type: DataTypes) -> Vec<String>{
        let mut response = Vec::new();
        let data_list = self.alarms.lock().unwrap().clone();
        for item in data_list{
            response.push(format!("{}", item))
        }
        response
    }
}

#[post("/assistant", format = "json", data = "<content>")]
fn assistant_post(content: Json<AssistantRequest>, assistant: State<Assistant>) -> String{
    match assistant.add_from_request(content.0){
        Ok(_) => format!("Success"),
        Err(e) => format!("Failure: {}", e),
    }
}

#[get("/assistant/alarms")]
fn assistant_get_alarms(assistant: State<Assistant>) -> Json<AssistantResponse>{
    Json(AssistantResponse {
        response_type: DataTypes::AlarmType,
        content: assistant.generate_response(DataTypes::AlarmType)
    })
}

#[post("/watchdog", format = "plain", data = "<data>")]


fn rocket() -> Rocket{
    let assistant = Assistant::new();
    rocket::ignite()
        .mount("/", routes![assistant_post, assistant_get_alarms])
        .manage(assistant)
}

fn main() {
    rocket().launch();
}
