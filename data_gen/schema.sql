CREATE TABLE IF NOT EXISTS "camper" (
	"camperID" integer,
	"fname" string,
	"lname" string,
	"phoneNum" integer,
	"medicalCond" string,
	"age" integer,
	"address" string,
	"gender" boolean,
	"emergencyContact" string,
	PRIMARY KEY ("camperID")
);

CREATE TABLE IF NOT EXISTS "campsite" (
	"campsiteID" integer,
	"location" string,
	"capacity" integer,
	"amenities" string,
	"availability" boolean,
	"dailyprice" integer,
	PRIMARY KEY ("campsiteID")
);

CREATE TABLE IF NOT EXISTS "activity" (
	"activityID" integer,
	"name" string,
	"description" string,
	"time" time,
	"location" string,
	"cost" integer,
	"date" date,
	"staffID" integer,
	PRIMARY KEY ("activityID"),
	FOREIGN KEY ("staffID") REFERENCES "staff" ("staffID")
            ON UPDATE RESTRICT
            ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS "staff" (
	"staffID" integer,
	"fname" string,
	"lname" string,
	"phoneNum" integer,
	"address" string,
	"role" string,
	PRIMARY KEY ("staffID")
);

CREATE TABLE IF NOT EXISTS "equipment" (
	"equipmentID" integer,
	"name" string,
	"quantity" integer,
	"condition" string,
	"availability" boolean,
	"cost" ,
	PRIMARY KEY ("equipmentID")
);

CREATE TABLE IF NOT EXISTS "reservation" (
	"reservationID" integer,
	"camperID" integer,
	"campsiteID" integer,
	"checkin" date,
	"checkout" date,
	"totalCost" integer,
	"reservationDate" date,
	PRIMARY KEY ("reservationID"),
	FOREIGN KEY ("camperID") REFERENCES "camper" ("camperID")
            ON UPDATE RESTRICT
            ON DELETE RESTRICT,
	FOREIGN KEY ("campsiteID") REFERENCES "campsite" ("campsiteID")
            ON UPDATE RESTRICT
            ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS "feedback" (
	"feedbackID" integer,
	"rating" decimal,
	"comment" string,
	"date" date,
	"camperID" integer,
	PRIMARY KEY ("feedbackID"),
	FOREIGN KEY ("camperID") REFERENCES "camper" ("camperID")
            ON UPDATE RESTRICT
            ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS "payment" (
	"paymentID" integer,
	"amount" float,
	"paymentMethod" string,
	"payDate" date,
	"reservationID" integer,
	PRIMARY KEY ("paymentID"),
	FOREIGN KEY ("reservationID") REFERENCES "reservation" ("reservationID")
            ON UPDATE RESTRICT
            ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS "activityEq" (
	"activityID" integer,
	"equipmentID" integer,
	FOREIGN KEY ("activityID") REFERENCES "activity" ("activityID")
            ON UPDATE RESTRICT
            ON DELETE RESTRICT,
	FOREIGN KEY ("equipmentID") REFERENCES "equipment" ("equipmentID")
            ON UPDATE RESTRICT
            ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS "camperEq" (
	"camperID" integer,
	"equipmentID" integer,
	"rentDate" date,
	"returnDate" date,
	"expectedReturnDate" date,
	FOREIGN KEY ("camperID") REFERENCES "camper" ("camperID")
            ON UPDATE RESTRICT
            ON DELETE RESTRICT,
	FOREIGN KEY ("equipmentID") REFERENCES "equipment" ("equipmentID")
            ON UPDATE RESTRICT
            ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS "activityRes" (
	"activityResID" integer,
	"reservationID" integer,
	"activityID" integer,
	PRIMARY KEY ("activityResID"),
	FOREIGN KEY ("reservationID") REFERENCES "reservation" ("reservationID")
            ON UPDATE RESTRICT
            ON DELETE RESTRICT,
	FOREIGN KEY ("activityID") REFERENCES "activity" ("activityID")
            ON UPDATE RESTRICT
            ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS "generalEq" (
	"equipmentID" integer,
	"category" string,
	FOREIGN KEY ("equipmentID") REFERENCES "equipment" ("equipmentID")
            ON UPDATE RESTRICT
            ON DELETE RESTRICT
);

