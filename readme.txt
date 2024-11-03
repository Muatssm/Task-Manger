You Need To Use The Project
MySQL needs
DataBase name : "task_manger"
2 Tables needs
First Table:
Name: `users` 
query = "CREATE TABLE `users` (
 `user_id` int(11) NOT NULL AUTO_INCREMENT,
 `username` varchar(40) DEFAULT NULL,
 `email` varchar(60) DEFAULT NULL,
 `password` varchar(12) DEFAULT NULL,
 `role` varchar(5) DEFAULT 'user',
 PRIMARY KEY (`user_id`),
 UNIQUE KEY `username` (`username`),
 UNIQUE KEY `email` (`email`),
 UNIQUE KEY `password` (`password`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4"
 
Second Table:
Name: `tasks`
query = "CREATE TABLE `tasks` (
 `task_id` int(11) NOT NULL AUTO_INCREMENT,
 `title` varchar(40) DEFAULT 'Normal Task',
 `description` varchar(70) DEFAULT 'No Description',
 `status` varchar(45) DEFAULT 'pending',
 `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
 `task_user_id` int(11) NOT NULL,
 PRIMARY KEY (`task_id`),
 KEY `user_tasks` (`task_user_id`),
 CONSTRAINT `user_tasks` FOREIGN KEY (`task_user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4"

The Features:
1 - Each user has tasks specific to his account and cannot modify the tasks of other users
2 - The User How have admin or owner role Can Edit on Tasks For all users
3 - tasks operations :
  | Add New Task
  | Edit Task Status
  | Delete Specfic Task
  | Show All Tasks