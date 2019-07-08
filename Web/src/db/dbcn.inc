<?php
    //连接数据库
    $db = new pdo("sqlite:/db/db.sqlite");
    if ($db){
        // to do ...
    }else{
        echo 'connect bad';
    }
?>
