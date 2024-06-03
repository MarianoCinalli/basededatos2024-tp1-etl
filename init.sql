-- Book Name,Author,Pages,Language,Ratings,Total Ratings,Price,Category
-- 11 Rules For Life: Secrets to Level Up,Chetan Bhagat,256,English,4.5,735,183,Self Improvement

CREATE TABLE IF NOT EXISTS `authors`(
    `author` VARCHAR(191) PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS `languages`(
    `language` VARCHAR(191) PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS `categories`(
    `category` VARCHAR(191) PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS `books`(
    `name` VARCHAR(191),
    `authorId` VARCHAR(191),
    `pages` INTEGER,
    `languageId` VARCHAR(191),
    `ratings` FLOAT,
    `totalRatings` INTEGER,
    `price` FLOAT,
    `categoryId` VARCHAR(191),
    PRIMARY KEY (`name`, `authorId`),
    FOREIGN KEY (`authorId`) REFERENCES `authors`(`author`),
    FOREIGN KEY (`languageId`) REFERENCES `languages`(`language`),
    FOREIGN KEY (`categoryId`) REFERENCES `categories`(`category`)
);
