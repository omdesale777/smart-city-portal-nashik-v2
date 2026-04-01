-- ═══════════════════════════════════════════════════════════════
-- Smart City Nashik — Seed Data
-- Paste this entire file into Supabase → SQL Editor → Run
-- Run AFTER the CREATE TABLE statements in database.py
-- ═══════════════════════════════════════════════════════════════


-- ─────────────────────────────────────────
-- HOTELS
-- ─────────────────────────────────────────
INSERT INTO hotels (id, name, area, stars, price_from, phone, tags, website) VALUES
  (gen_random_uuid(), 'Radisson Blu Nashik',          'College Road, Nashik',               5, 4500,  '02536699999',  ARRAY['Luxury','Pool','Spa','Restaurant','Conference'], 'https://www.radissonhotels.com'),
  (gen_random_uuid(), 'The Byke Grassroot',           'Gangapur Road, Nashik',              4, 2800,  '02532388888',  ARRAY['Heritage','Gardens','Banquet','Bar'],             'https://thebyke.com'),
  (gen_random_uuid(), 'Sula The Source Resort',       'Govardhan Village, Nashik',          4, 6500,  '02532505000',  ARRAY['Vineyard Resort','Pool','Wine Tours','Spa'],      'https://thesource.sulawines.com'),
  (gen_random_uuid(), 'Hotel Express Inn',            'Ambad, Nashik',                      4, 2200,  '02532382222',  ARRAY['Business','Restaurant','Free WiFi','Parking'],    NULL),
  (gen_random_uuid(), 'Panchavati Yatri Niwas',       'Near Kalaram Temple, Panchavati',    3, 900,   '02532500000',  ARRAY['Pilgrim Stay','AC Rooms','Satvik Food'],          NULL),
  (gen_random_uuid(), 'Hotel Panchavati',             'Old Agra Road, Nashik',              3, 1200,  '02532310000',  ARRAY['Budget','Central Location','24hr Desk'],         NULL),
  (gen_random_uuid(), 'Hotel Ibis Nashik',            'Pathardi Phata, Nashik',             3, 1800,  '02536620000',  ARRAY['Modern','Free WiFi','Restaurant','AC'],           'https://ibis.accor.com'),
  (gen_random_uuid(), 'Dharamshala Trimbakeshwar',    'Near Trimbakeshwar Temple, Trimbak', 2, 300,   '02594233033',  ARRAY['Pilgrim Lodge','Basic','Walk to Temple'],         NULL),
  (gen_random_uuid(), 'MTDC Resort Nashik',           'Near Gangapur Dam, Nashik',          3, 1400,  '02532511222',  ARRAY['Government','Gardens','Restaurant','Safe'],       'https://mtdcresorts.com'),
  (gen_random_uuid(), 'OYO Townhouse CBS Nashik',     'CBS Road, Nashik',                   2, 700,   NULL,           ARRAY['Budget','Central','Walk to CBS'],                 NULL);


-- ─────────────────────────────────────────
-- SPIRITUAL SPOTS
-- ─────────────────────────────────────────
INSERT INTO spiritual_spots (id, name, name_deva, category, description, address, gps_lat, gps_lng, timings, entry_fee, image_url, rating) VALUES
  (gen_random_uuid(),
   'Trimbakeshwar Shiva Temple',
   'श्री त्र्यंबकेश्वर ज्योतिर्लिंग मंदिर',
   'Jyotirlinga Temple',
   'One of the 12 sacred Jyotirlingas. Birthplace of the Godavari River at Brahmagiri Hill. Built by Peshwa Balaji Bajirao (1740–60 CE). The unique three-faced Shivalinga here represents Brahma, Vishnu, and Shiva. Rare rituals like Narayan Nagbali and Kalsarpa Shanti are performed only at Trimbakeshwar.',
   'Trimbak, Nashik district, Maharashtra 422212',
   19.9338, 73.5303,
   '6:00 AM – 9:00 PM',
   'Free (VIP darshan available)',
   'https://commons.wikimedia.org/wiki/Special:FilePath/Trimbakeshwar_img_1.JPG',
   4.9),

  (gen_random_uuid(),
   'Kalaram Temple',
   'श्री काळाराम मंदिर, पंचवटी',
   'Hindu Temple',
   'Built in 1792 by Sardar Rangarao Odhekar with 2,000 workers over 12 years. Houses the black-stone idol of Lord Rama discovered in the Godavari River. Temple summit is plated with 32 tonnes of gold. Historic site of Dr. B.R. Ambedkar''s Satyagraha for Dalit temple entry rights (1930–1935).',
   'Panchavati, Nashik, Maharashtra 422003',
   20.0013, 73.7874,
   '5:30 AM – 10:00 PM',
   'Free',
   'https://commons.wikimedia.org/wiki/Special:FilePath/Sri_Kalaram_Mandir_Sansthan,_Panchavati,_Nashik.jpg',
   4.8),

  (gen_random_uuid(),
   'Ramkund',
   'रामकुंड · पंचवटी',
   'Holy Ghat',
   'The holiest ghat in Nashik on the Godavari River. Believed to be where Lord Rama bathed during his 14-year exile. The sacred Asthivilaya Kund here dissolves bones and ashes — prominent figures including Nehru and Indira Gandhi had their ashes immersed here. Primary venue for Simhastha Kumbh Mela every 12 years.',
   'Ramkund, Panchavati, Nashik 422003',
   20.0019, 73.7891,
   'Open 24 hours',
   'Free',
   'https://commons.wikimedia.org/wiki/Special:FilePath/Ramkund,nashik.JPG',
   4.7),

  (gen_random_uuid(),
   'Saptashringi Devi Temple',
   'श्री सप्तश्रृंगी देवी, वणी',
   'Shakti Peeth',
   'One of Maharashtra''s three and a half Shakti Peethas. Perched on seven sacred peaks (Sapta Shringas) at 4,659 feet in Vani, 65 km from Nashik. The 18-armed deity Saptashringi is revered as Adi Shakti. The journey involves 472 steps. A ropeway is also available.',
   'Vani, Nashik district, Maharashtra 423204',
   20.4056, 73.8258,
   '5:00 AM – 10:00 PM',
   'Free (ropeway: ₹120)',
   'https://commons.wikimedia.org/wiki/Special:FilePath/Saptashrungi_temple_nashik.jpg',
   4.8),

  (gen_random_uuid(),
   'Muktidham Temple',
   'मुक्तिधाम मंदिर',
   'Temple Complex',
   'Stunning white Rajasthani marble complex near Nashik Road. Features replicas of all 12 Jyotirlinga shrines and all 18 chapters of the Bhagavad Gita inscribed on its walls in Sanskrit. The Makrana marble used is the same as the Taj Mahal.',
   'Muktidham Colony, Nashik Road, Nashik 422101',
   19.9602, 73.8290,
   '7:00 AM – 9:00 PM',
   'Free',
   'https://commons.wikimedia.org/wiki/Special:FilePath/Muktidham_Temple_Nashik.jpg',
   4.5),

  (gen_random_uuid(),
   'Someshwar Temple',
   'सोमेश्वर मंदिर · गोदावरी घाट',
   'Shiva Temple',
   'Serene Shiva temple on the Godavari riverbank, 8 km from Nashik city. Famous for the natural waterfall adjacent to it. Peaceful ghats ideal for early-morning prayer. During Shravan month devotees perform special abhishek rituals here.',
   'Gangapur Road, Nashik, Maharashtra 422013',
   20.0271, 73.7602,
   '6:00 AM – 8:00 PM',
   'Free',
   'https://commons.wikimedia.org/wiki/Special:FilePath/Someshwar_mandir,nashik.JPG',
   4.5),

  (gen_random_uuid(),
   'Pandavleni Caves',
   'पांडवलेणी · त्रिरश्मी गुहा',
   'Buddhist Heritage',
   '24 rock-cut Buddhist caves on Trirashmi Hill, carved between 1st century BCE and 2nd century CE. Cave 18 is a chaitya prayer hall. Intricate Hinayana sculptures and ancient inscriptions preserved for over 2,000 years. Protected ASI monument.',
   'Trirashmi Hill, NH-3, Nashik 422101',
   19.9710, 73.8380,
   '6:00 AM – 6:00 PM',
   '₹30 (Indian) / ₹300 (Foreign)',
   'https://commons.wikimedia.org/wiki/Special:FilePath/Pandav_leni_caves_nashik.jpg',
   4.6);


-- ─────────────────────────────────────────
-- SPIRITUAL EVENTS
-- ─────────────────────────────────────────
INSERT INTO spiritual_events (id, name, icon, when_text, description) VALUES
  (gen_random_uuid(), 'Simhastha Kumbh Mela',   '🪔', 'Every 12 Years (Next: 2027)',  'The largest religious gathering on Earth at Ramkund on the Godavari. Millions of pilgrims take a holy Shahi Snan. Last held in 2015; next in 2027.'),
  (gen_random_uuid(), 'Ram Navami',             '🌸', 'March – April',                'Birthday of Lord Rama celebrated with grand Rath Yatra processions from Kalaram Temple. Thousands participate in bhajans and rituals through Panchavati.'),
  (gen_random_uuid(), 'Ganesh Chaturthi',       '🥁', 'August – September',           '10-day festival with spectacular pandals and the immersion of Lord Ganesha''s idol into the Godavari River at Ramkund ghat.'),
  (gen_random_uuid(), 'Navratri at Saptashringi','🕯️','October – November',           'Nine nights of celebrations at Saptashringi Devi Temple in Vani. Special puja, aarti, and cultural events with lakhs of devotees.'),
  (gen_random_uuid(), 'SulaFest',               '🍷', 'February',                     'India''s premier music and wine festival at Sula Vineyards — two days of live performances, wine tasting, and glamping in the vineyard.'),
  (gen_random_uuid(), 'Shravan Somvar',         '🌊', 'Every Monday (Shravan month)', 'During the holy month of Shravan, thousands visit Trimbakeshwar and Someshwar for special Monday puja and abhishek to Lord Shiva.');


-- ─────────────────────────────────────────
-- TOURIST SPOTS (Bhatakanti)
-- ─────────────────────────────────────────
INSERT INTO tourist_spots (id, name, category, description, address, distance_km, difficulty, entry_fee, timings, image_url, map_link, youtube_link, rating) VALUES

  -- FORTS
  (gen_random_uuid(),
   'Harihar Fort', 'fort',
   'The most thrilling fort trek in Maharashtra. 80° near-vertical rock-cut steps carved into the cliff face require hands and feet both. At the summit — panoramic 360° views of the entire Sahyadri range. Also called Harshagad.',
   'Nirgudpada Village, Nashik district',
   40, 'hard', 'Free', 'Sunrise to Sunset',
   'https://commons.wikimedia.org/wiki/Special:FilePath/Harihar_Fort_Maharashtra.jpg',
   'https://maps.google.com/?q=Harihar+Fort+Nashik',
   'https://www.youtube.com/results?search_query=Harihar+Fort+Trek+Nashik',
   4.8),

  (gen_random_uuid(),
   'Salher Fort', 'fort',
   'The highest fort in Maharashtra at 5,322 ft. Site of the decisive Battle of Salher (1672) — first major open-field Maratha victory over the Mughals. Twin peaks Salher and Salota connected by a saddle ridge.',
   'Baglan, Nashik district',
   110, 'hard', 'Free', 'Sunrise to Sunset',
   NULL,
   'https://maps.google.com/?q=Salher+Fort+Nashik',
   'https://www.youtube.com/results?search_query=Salher+Fort+Trek+Nashik',
   4.7),

  (gen_random_uuid(),
   'Rajdher Fort', 'fort',
   'Well-preserved Yadava-era fort with ruins of temples, cisterns, and old cannons. Often combined with nearby Moragad fort. A hidden gem for history enthusiasts seeking an uncrowded trek.',
   'Peint, Nashik district',
   70, 'moderate', 'Free', 'Sunrise to Sunset',
   NULL,
   'https://maps.google.com/?q=Rajdher+Fort+Nashik',
   'https://www.youtube.com/results?search_query=Rajdher+Fort+Nashik+trek',
   4.4),

  -- WATERFALLS
  (gen_random_uuid(),
   'Dugarwadi Falls', 'waterfall',
   'Nashik''s most spectacular waterfall — a 165-ft cascade through dense forest near Igatpuri. Requires a 45-minute jungle trek. Swimming allowed in the natural plunge pool. Accessible and spectacular only during monsoon.',
   'Near Igatpuri, Nashik district',
   55, 'easy', 'Free', 'July to October (monsoon)',
   'https://commons.wikimedia.org/wiki/Special:FilePath/Dugarwadi_waterfall_nashik.jpg',
   'https://maps.google.com/?q=Dugarwadi+Waterfall+Igatpuri',
   'https://www.youtube.com/results?search_query=Dugarwadi+Waterfall+Nashik',
   4.6),

  (gen_random_uuid(),
   'Someshwar Falls', 'waterfall',
   'Natural waterfall beside the Someshwar Shiva Temple on the Godavari. Just 8 km from the city — no trekking required. Popular for family picnics during monsoon.',
   'Gangapur Road, 8 km from CBS Nashik',
   8, 'easy', 'Free', 'July to October',
   'https://commons.wikimedia.org/wiki/Special:FilePath/Someshwar_mandir,nashik.JPG',
   'https://maps.google.com/?q=Someshwar+Waterfall+Nashik',
   'https://www.youtube.com/results?search_query=Someshwar+waterfall+Nashik',
   4.4),

  (gen_random_uuid(),
   'Umbrella Falls', 'waterfall',
   'Fan-shaped waterfall near Igatpuri that spreads like an open umbrella during monsoon. Accessible right off the Mumbai–Nashik highway — no trekking required.',
   'Near Igatpuri, off Mumbai–Nashik Highway',
   55, 'easy', 'Free', 'July to September',
   NULL,
   'https://maps.google.com/?q=Umbrella+Falls+Igatpuri+Nashik',
   'https://www.youtube.com/results?search_query=Umbrella+Falls+Igatpuri',
   4.5),

  -- ADVENTURE
  (gen_random_uuid(),
   'Brahmagiri Trek', 'adventure',
   'Sacred hill above Trimbakeshwar where the Godavari originates. A 4 km circular trek through dense forest leads to Kushavarta Kund at 4,248 ft. Spiritually significant and scenically stunning; sunrise from the summit is breathtaking.',
   'Trimbakeshwar, 28 km from Nashik',
   28, 'moderate', 'Free', 'Sunrise to Sunset',
   'https://commons.wikimedia.org/wiki/Special:FilePath/Brahmagiri_hills,_Trimbakeshwar.jpg',
   'https://maps.google.com/?q=Brahmagiri+Hill+Trimbakeshwar',
   'https://www.youtube.com/results?search_query=Brahmagiri+Trek+Nashik',
   4.7),

  (gen_random_uuid(),
   'Igatpuri Adventure Zone', 'adventure',
   'Nashik''s adventure capital — paragliding, valley crossing, rappelling, camping, and kayaking on the Bhavali reservoir. Bhavali Dam, Dugarwadi Falls, and Tringalwadi Fort are nearby.',
   'Igatpuri, Nashik district',
   55, 'moderate', 'Varies by activity', 'Year-round',
   NULL,
   'https://maps.google.com/?q=Igatpuri+Maharashtra',
   'https://www.youtube.com/results?search_query=Igatpuri+adventure+paragliding+Nashik',
   4.6),

  -- NATURE
  (gen_random_uuid(),
   'Nandur Madhmeshwar Bird Sanctuary', 'nature',
   'Ramsar-listed wetland sanctuary 45 km from Nashik. Home to 230+ bird species including flamingos, painted storks, and migratory waterfowl from Central Asia. Best October–February when migratory birds arrive.',
   'Niphad, Nashik district',
   45, 'easy', '₹50', '6:00 AM – 6:00 PM',
   NULL,
   'https://maps.google.com/?q=Nandur+Madhmeshwar+Bird+Sanctuary',
   'https://www.youtube.com/results?search_query=Nandur+Madhmeshwar+bird+sanctuary+Nashik',
   4.5),

  (gen_random_uuid(),
   'Gangapur Dam', 'nature',
   'Picturesque reservoir on the Godavari, 10 km from Nashik. Popular for sunrise views, boat rides, and picnics. Backwaters stretch for kilometres — stunning during monsoon overflow.',
   'Gangapur, 10 km from Nashik',
   10, 'easy', 'Free', '6:00 AM – 6:00 PM',
   'https://commons.wikimedia.org/wiki/Special:FilePath/Gangapur_Dam_Nashik.JPG',
   'https://maps.google.com/?q=Gangapur+Dam+Nashik',
   'https://www.youtube.com/results?search_query=Gangapur+Dam+Nashik',
   4.3),

  -- HISTORY
  (gen_random_uuid(),
   'Coin Museum (IIRNS)', 'history',
   'Asia''s only dedicated coin museum at the Indian Institute of Research in Numismatic Studies. Over 1 lakh coins spanning 2,500 years — from ancient punch-marked coins to modern Indian currency. A completely unique, underrated attraction.',
   'Anjaneri, Trimbakeshwar Road, 30 km from Nashik',
   30, 'easy', '₹20', '10:00 AM – 5:00 PM (Closed Mon)',
   NULL,
   'https://maps.google.com/?q=IIRNS+Coin+Museum+Nashik',
   'https://www.youtube.com/results?search_query=IIRNS+Coin+Museum+Nashik',
   4.5),

  (gen_random_uuid(),
   'Darna Dam', 'history',
   'One of India''s oldest operational gravity dams, built in 1911 during British colonial rule on the Darna River. Surrounded by forested Sahyadri hills. Beautiful during monsoon overflow. Leopard sightings reported in the surrounding jungle.',
   'Darna village, 70 km from Nashik',
   70, 'easy', 'Free', 'Open all day',
   NULL,
   'https://maps.google.com/?q=Darna+Dam+Nashik',
   'https://www.youtube.com/results?search_query=Darna+Dam+Nashik',
   4.3);


-- ─────────────────────────────────────────
-- VERIFY: row counts
-- ─────────────────────────────────────────
SELECT 'hotels'         AS table_name, COUNT(*) AS rows FROM hotels
UNION ALL
SELECT 'spiritual_spots',              COUNT(*)         FROM spiritual_spots
UNION ALL
SELECT 'spiritual_events',             COUNT(*)         FROM spiritual_events
UNION ALL
SELECT 'tourist_spots',                COUNT(*)         FROM tourist_spots;