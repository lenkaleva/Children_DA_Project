CREATE OR REPLACE TABLE T01_INPUT_UNION AS

SELECT 

    "countryno" AS "country_no",
    "surveyyear" AS "year",
    "uniqueid" AS "pupil_no",
    "schoolno" AS "school_no",
    CAST(TRY_CAST(REPLACE(TRIM("age"), ',', '.') AS NUMBER) AS INT) AS "age",
    "sex",
    "famcar" AS "fam_car",
    CASE 
      WHEN "bedroom" = '1' THEN 0
      WHEN "bedroom" = '2' THEN 1
      ELSE NULL
    END AS "own_bedroom_flag",
    "computers" AS "computer_no",
    "health",
    "headache",
    "stomachache",
    "lifesat",
    "feellow"      AS "feel_low",
    "nervous",
    "sleepdifficulty" AS "sleep_dif",
    "dizzy",
    "thinkbody"     AS "think_body",
    "physact60"     AS "phys_act_60",
    "breakfastwd"   AS "breakfast_weekdays",
    "breakfastwe"   AS "breakfast_weekend",
    "fruits"      AS "fruits",
    "vegetables"  AS "vegetables",
    "sweets"      AS "sweets",
    "softdrinks"  AS "soft_drinks",
    NULL         AS "family_meals_together",
    "toothbr"       AS "tooth_brushing",
    NULL AS "time_exe",
    NULL AS "alcohol_lifetime",
    NULL AS "alcohol_30",
    "cannabisltm" AS "cannabis_lifetime",
    NULL AS "cannabis_30",
    "drunk"      AS "drunk_30",
    NULL AS "overweight",
    "mbmi" as "BMI",
    NULL AS "fam_support",
    NULL AS "fam_help",
    "talkmother" as "talk_mother",
    "talkfather" as "talk_father",
case when "fatherhome1" = '2' then 0
     WHEN "fatherhome1" = '1' THEN 1
     else NULL end
    as "father_home_flag" ,
 case when "motherhome1" = '2' then 0 
      WHEN "motherhome1" = '1' THEN 1
      else NULL end
    as "mother_home_flag" ,
-1 AS "social_media_flag",
NULL as "feelings_online",
NULL as "secrets_online",
NULL as "online_group",
NULL as "Online_friend",
"talkbestfriend" AS "friend_talk",
NULL AS "friend_help",
"injured12m" as "injured_year",
"fight12m" as "fight_year",
NULL AS "cyber_bul_been",
NULL AS "cyber_bul_others",
"beenbullied" as "bul_been",
"bulliedothers" as "bul_others",
NULL AS "teacher_cares",
NULL AS "teacher_accepts",
NULL AS "stud_accepts",
"studtogether" as "stud_together",
"schoolpressure" as "school_pressure",
"likeschool" as "like_school",
"bodyheight" as "body_hight",
"bodyweight" as "body_weight"
FROM HBSC_2001

UNION

SELECT 
    "countryno" AS "country_no",
    "surveyyear" as "year",
    "uniqueid" AS "pupil_no",
    "schoolno" AS "school_no",
    CAST(TRY_CAST(REPLACE(TRIM("age"), ',', '.') AS NUMBER) AS INT) AS "age",
    "sex",
    "famcar" AS "fam_car",
    CASE 
      WHEN "bedroom" = '1' THEN 0
      WHEN "bedroom" = '2' THEN 1
      ELSE NULL
    END AS "own_bedroom_flag",
    "computers" AS "computer_no",
    "health",
    "headache",
    "stomachache",
    "lifesat",
    "feellow"      AS "feel_low",
    "nervous",
    "sleepdifficulty" AS "sleep_dif",
    "dizzy",
    "thinkbody"     AS "think_body",
    "physact60"     AS "phys_act_60",
    "breakfastwd"   AS "breakfast_weekdays",
    "breakfastwe"   AS "breakfast_weekend",
    "fruits"      AS "fruits",
    "vegetables"  AS "vegetables",
    "sweets"      AS "sweets",
    "softdrinks"  AS "soft_drinks",
    null        AS "family_meals_together",
    "toothbr"       AS "tooth_brushing",
    "timeexce"       AS "time_exe",
    "alcopops"        AS "alcohol_lifetime",
    null     AS "alcohol_30",
    "cannabisltm" AS "cannabis_lifetime",
    "cannabis30d" AS "cannabis_30",
    "drunk"      AS "drunk_30",
    null AS "overweight",
    null as "BMI",
    null as "fam_support",
    null as "fam_help",
    "talkmother" as "talk_mother",
    "talkfather" as "talk_father",
case when "fatherhome1" = '2' then 0 
        when "fatherhome1" = '1' then 1
     else null end
    as "father_home_flag" ,
 case when "motherhome1" = '2' then 0 
      else "motherhome1" end
    as "mother_home_flag" ,
  -1  as "social_media_flag",
null as "feelings_online",
null as "secrets_online",
null as "online_group",
null as "Online_friend",
"talkbestfriend" as "friend_talk",
null as "friend_help",
"injured12m" as "injured_year",
"fight12m" as "fight_year",
null as "cyber_bul_been",
null as "cyber_bul_others",
"beenbullied" as "bul_been",
"bulliedothers" as "bul_others",
"acachieve" as "teacher_cares",
null as "teacher_accepts",
"studaccept" as "stud_accepts",
"studtogether" as "stud_together",
"schoolpressure" as "school_pressure",
"likeschool" as "like_school",
"bodyheight" as "body_hight",
"bodyweight" as "body_weight"
FROM HBSC_2006

UNION

SELECT 
    "countryno" AS "country_no",
    "surveyyear" as "year",
    "uniqueid" AS "pupil_no",
    "schoolno" AS "school_no",
    CAST(TRY_CAST(REPLACE(TRIM("age"), ',', '.') AS NUMBER) AS INT) AS "age",
    "sex",
    "famcar" AS "fam_car",
    CASE 
      WHEN "bedroom" = '1' THEN 0
      WHEN "bedroom" = '2' THEN 1
      ELSE NULL
    END AS "own_bedroom_flag",
    "computers" AS "computer_no",
    "health",
    "headache",
    "stomachache",
    "lifesat",
    "feellow" AS "feel_low",
    "nervous",
    "sleepdifficulty" AS "sleep_dif",
    "dizzy",
    "thinkbody"     AS "think_body",
    "physact60"     AS "phys_act_60",
    "breakfastwd"   AS "breakfast_weekdays",
    "breakfastwe"   AS "breakfast_weekend",
    "fruits"      AS "fruits",
    "vegetables"  AS "vegetables",
    "sweets"      AS "sweets",
    "softdrinks"  AS "soft_drinks",
    null         AS "family_meals_together",
    "toothbr"       AS "tooth_brushing",
    "timeexce"       AS "time_exe",
    "alcopops"        AS "alcohol_lifetime",
    "drink30d"     AS "alcohol_30",
    "cannabisltm" AS "cannabis_lifetime",
    "cannabis30d" AS "cannabis_30",
    "drunk30d"      AS "drunk_30",
     null AS "overweight",
    "MBMI" as "BMI",
    null as "fam_support",
    null as "fam_help",
    "talkmother" as "talk_mother",
    "talkfather" as "talk_father",
case when "fatherhome1" = '2' then 0 
    when "fatherhome1" = '1' then 1
     else null end
    as "father_home_flag" ,
 case when "motherhome1" = '2' then 0 
      when "motherhome1" = '1' then 1  
     else null end
    as "mother_home_flag" ,
-1 as "social_media_flag",
null as "feelings_online",
null as "secrets_online",
null as "online_group",
null as "Online_friend",
"talkbestfriend" as "friend_talk",
null as "friend_help",
"injured12m" as "injured_year",
"fight12m" as "fight_year",
null as "cyber_bul_been",
null as "cyber_bul_others",
"beenbullied" as "bul_been",
"bulliedothers" as "bul_others",
"acachieve" as "teacher_cares",
null as "teacher_accepts",
"studaccept" as "stud_accepts",
"studtogether" as "stud_together",
"schoolpressure" as "school_pressure",
"likeschool" as "like_school",
"bodyheight" as "body_hight",
"bodyweight" as "body_weight"
FROM HBSC_2010

UNION

SELECT 

    "COUNTRYno" AS "country_no",
    "HBSC" AS "year",
    "id4" AS "pupil_no",
    "id2" AS "school_no",
    CAST(TRY_CAST(REPLACE(TRIM("AGE"), ',', '.') AS NUMBER) AS INT) AS "age",
    "sex",
    "fasfamcar" AS "fam_car",
    CASE 
      WHEN "fasbedroom" = '1' THEN 0
      WHEN "fasbedroom" = '2' THEN 1
      ELSE NULL
    END AS "own_bedroom_flag",
    "fascomputers" AS "computer_no",
    "health",
    "headache",
    "stomachache",
    "lifesat",
    "feellow"      AS "feel_low",
    "nervous",
    "sleepdificulty" AS "sleep_dif",
    "dizzy",
    "thinkbody"     AS "think_body",
    "physact60"     AS "phys_act_60",
    "breakfastwd"   AS "breakfast_weekdays",
    "breakfastwe"   AS "breakfast_weekend",
    "fruits"      AS "fruits",
    "vegetables"  AS "vegetables",
    "sweets"      AS "sweets",
    "softdrinks"  AS "soft_drinks",
    "m12"         AS "family_meals_together",
    "toothbr"       AS "tooth_brushing",
    "timeexe"       AS "time_exe",
    "alcltm"        AS "alcohol_lifetime",
    "alc30d_2"     AS "alcohol_30",
    "cannabisltm_2" AS "cannabis_lifetime",
    "cannabis30d_2" AS "cannabis_30",
    "drunk30d"      AS "drunk_30",
    NULL AS "overweight",
    "MBMI" as "BMI",
    "famsup" as "fam_support",
    "famhelp" as "fam_help",
    "talkmother" as "talk_mother",
    "talkfather" as "talk_father",
case when "fatherhome1" = '2' then 0
     WHEN "fatherhome1" = '1' THEN 1
     else NULL end
    as "father_home_flag" ,
 case when "motherhome1" = '2' then 0 
      WHEN "motherhome1" = '1' THEN 1
      else NULL end
    as "mother_home_flag" ,
-1 AS "social_media_flag",
NULL as "feelings_online",
NULL as "secrets_online",
NULL as "online_group",
NULL as "Online_friend",
"friendtalk" as "friend_talk",
"friendhelp" as "friend_help",
"injured12m" as "injured_year",
"fight12m" as "fight_year",
"cbullmess" as "cyber_bul_been",
NULL AS "cyber_bul_others",
"beenbullied" as "bul_been",
"bulliedothers" as "bul_others",
"teachercare" as "teacher_cares",
"teacheraccept" as "teacher_accepts",
"studaccept" as "stud_accepts",
"studtogether" as "stud_together",
"schoolpressure" as "school_pressure",
"likeschool" as "like_school",
"bodyheight" as "body_hight",
"bodyweight" as "body_weight"
FROM HBSC_2014

UNION

SELECT 
    "countryno" AS "country_no",
    "HBSC" AS "year",
    "id4" AS "pupil_no",
    "id2" AS "school_no",
    CAST(TRY_CAST(REPLACE(TRIM("age"), ',', '.') AS NUMBER) AS INT) AS "age",
    "sex",
    "fasfamcar" AS "fam_car",
    CASE 
      WHEN "fasbedroom" = '1' THEN 0
      WHEN "fasbedroom" = '2' THEN 1
      ELSE NULL
    END AS "own_bedroom_flag",
    "fascomputers" AS "computer_no",
    "health",
    "headache",
    "stomachache",
    "lifesat",
    "feellow"      AS "feel_low",
    "nervous",
    "sleepdificulty" AS "sleep_dif",
    "dizzy",
    "thinkbody"     AS "think_body",
    "physact60"     AS "phys_act_60",
    "breakfastwd"   AS "breakfast_weekdays",
    "breakfastwe"   AS "breakfast_weekend",
    "fruits_2"      AS "fruits",
    "vegetables_2"  AS "vegetables",
    "sweets_2"      AS "sweets",
    "softdrinks_2"  AS "soft_drinks",
    "fmeal"         AS "family_meals_together",
    "toothbr"       AS "tooth_brushing",
    "timeexe"       AS "time_exe",
    "alcltm"        AS "alcohol_lifetime",
    "alc30d_2"     AS "alcohol_30",
    "cannabisltm_2" AS "cannabis_lifetime",
    "cannabis30d_2" AS "cannabis_30",
    "drunkltm"      AS "drunk_30",
    "oweight_who" AS "overweight",
    "MBMI" as "BMI",
    "famsup" as "fam_support",
    "famhelp" as "fam_help",
    "talkmother" as "talk_mother",
    "talkfather" as "talk_father",
case when "fatherhome1" = '2' then 0
     WHEN "fatherhome1" = '1' THEN 1
     else NULL end
    as "father_home_flag" ,
 case when "motherhome1" = '2' then 0 
      WHEN "motherhome1" = '1' THEN 1
      else NULL end
    as "mother_home_flag" ,
  case when "emcsocmed1" = '1' then 0 
       when   "emcsocmed1" = '2' then 1
       when "emcsocmed1" = '99' then null
    else NULL end
    as "social_media_flag",
"emconlpref1" as "feelings_online",
"emconlpref2" as "secrets_online",
"emconlfreq2" as "online_group",
"emconlfreq1" as "Online_friend",
"friendtalk" as "friend_talk",
"friendhelp" as "friend_help",
"injured12m" as "injured_year",
"fight12m" as "fight_year",
"cbeenbullied" as "cyber_bul_been",
"cbulliedothers" as "cyber_bul_others",
"beenbullied" as "bul_been",
"bulliedothers" as "bul_others",
"teachercare" as "teacher_cares",
"teacheraccept" as "teacher_accepts",
"studaccept" as "stud_accepts",
"studtogether" as "stud_together",
"schoolpressure" as "school_pressure",
"likeschool" as "like_school",
"bodyheight" as "body_hight",
"bodyweight" as "body_weight"
FROM HBSC_2018;
