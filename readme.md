# Test Specification for Senior Backend Python Developer
Create a GraphQL to-do application (using Flask) that allows users to perform these actions after logging in:
*Create new item or items
*Query an item or items
*Query items based on status or due date
*Change the status of an item as in-progress or done
*Change the due date of an item
*Delete an item

## List of Users (to see users and their passwords!)
```graphql
query UserList {
  users {
    success
    errors
    users{
      id
      name
      username
      password
    }
	}
}
```

## Register (just in case)
```graphql
mutation Register {
  register(name:"Hamid", username:"hamid",password:"1") {
    success
    errors
    user {
      id
      name
      username
      password
    }
    token
  }
}
```

## Login
it return a bearer token that should be used in task queries 
```graphql
query Login {
  login(username:"behnam", password:"1") {
    success
    errors
    user {
      id
      name
      username
      password
    }
    token
  }
}
```
## Query an item
```graphql
query Task {
  task(id:"11") {
    success
    errors
    task{
      id
      user_id
      title
      description
      status
      due_date
    }
	}
}
```

## Query items
```graphql
query TaskList {
  tasks {
    success
    errors
    tasks{
      id
      user_id
      title
      description
      status
      due_date
    }
	}
}
```

## Query items based on status or due date
```graphql
query TaskList {
  tasks(status:TODO,due_date:"2020-01-01") {
    success
    errors
    tasks{
      id
      user_id
      title
      description
      status
      due_date
    }
	}
}
```

## Query items based on status or due date
```graphql
query TaskList {
  tasks(due_date:"2020-01-01") {
    success
    errors
    tasks{
      id
      user_id
      title
      description
      status
      due_date
    }
	}
}
```

## Query items based on status or due date
```graphql
query TaskList {
  tasks(status:DONE) {
    success
    errors
    tasks{
      id
      user_id
      title
      description
      status
      due_date
    }
	}
}
```

## Create new item
```graphql
mutation CreateTask {
  create_task(task:{title:"Task21",description:"What", due_date:"1-1-2020"}) {
    success
    errors
    task {
      id
      user_id
      title
      description
      status
      due_date
    }
  }
}
```

## Create new items
```graphql
mutation CreateTasks {
  create_tasks(tasks:[{title:"Task125",description:"1", due_date:"1-1-2020"},
                     {title:"Task126",description:"2", due_date:"1-2-2020"},
                     {title:"Task127",description:"3", due_date:"1-3-2020"}]) {
    success
    errors
    tasks {
      id
      user_id
      title
      description
      status
      due_date
    }
  }
}
```

## Change the status of an item as in-progress or done
```graphql
mutation UpdateTaskStatus {
  updateStatus(id:"5", newStatus:DONE) {
    success
    errors
    task{
      id
      user_id
      title
      description
      status
      due_date
    }
	}
}
```

## Change the due date of an item
```graphql
mutation UpdateTaskDueDate {
  updateDueDate(id:"5", newDate:"4-4-1994") {
    success
    errors
    task{
      id
      user_id
      title
      description
      status
      due_date
    }
	}
}
```

## Delete an item
```graphql
mutation deleteTask {
  deleteTask(id:"7") {
    success
    errors
	}
}
```