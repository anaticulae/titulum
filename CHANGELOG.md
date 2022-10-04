# Changelog

Every noteable change is logged here.

## v0.11.0

### Feature

* skip too many headlines on a single page (209ce3270cd7)
* limit headline font size (b4ab83f9fa25)
* improve headline lookup (b50cb370bf4c)

### Fix

* use improve test name generator (b83c6a5dcbf3)

## v0.10.0

### Feature

* do not drop result if no level one is given (45de9701bc18)
* extend debugging information (dac3bdf72c07)

### Fix

* do not skip data if no all levels are filled (4daa62a29a9d)

## v0.9.1

### Fix

* add missing import (b7970ceabd18)
* skip empty page data (706919e98e84)

## v0.9.0

### Feature

* skip invalid headlines (25c73448d42e)
* skip cluster with too many duplicated levels (e2050aabc84a)
* skip hidden items (4ef9fe053014)
* verify levelfour result (084cf5c40b4e)
* skip cluster with to many hidden lines (d88f8c8d0799)
* assign page and container for detected headlines (945e257c0077)
* use improved cluster (48bfc43cbcb8)
* use improved merger (c457999a487e)
* add visible column to improve parser result (b29f9daeeca2)
* load visible and invisible data (700f11b6b78b)
* use underline to merge headlines (82ff30e57e95)
* add underline as cluster attribute (3c037cbe1d76)
* log invalid multiline group (54ec147f9b6a)
* use level four headlines to improve result (c6cf6623306d)

### Fix

* stop after detecting headline end (a55495c56a91)
* find headline only once (f73e10c5ed0a)
* sort tuple correctly (b4e94d0beecb)
* score None result correctly (fd19e6271470)
* adjust check for empty data (817c73401c48)
* skip too few headlines (8b2a915a1430)
* skip multipart section as possible chapter section (e7de5feaf123)
* sorting headlines seams to be useless (8f61336ec8a5)
* after is already checked (b42c3ef7219f)
* inform about empty tests (100d64bab86a)

## v0.8.0

### Feature

* use levelfour result as input to improve result (3a7cce7b2641)
* do not treat valid headlines as level four headlines (ae3530b16feb)
* add levelfour step (4109e18c7d0b)
* add method to merge level four and check if exists (de30a41cfb6a)

## v0.7.1

### Feature

* use central headline length judger (024f56d940a3)

### Fix

* do not skip headlines at page end (53b87f4f0c16)
* fix error message (fdcdaf1bc39a)

## v0.7.0

### Feature

* use new datatype with strategy field (38dc024a5bb3)
* add method to convert to headline result (2e07168ad87d)
* disable result for too few headlines (171b65fe722e)
* add table with minimal headline count (1fe8b036574e)
* add left and right alignment check (90cdd68dbafc)

### Fix

* adjust headlines path (fef105b3dc4b)
* adjust filename, fix magic result value (ac79944df8d5)

## v0.6.0

### Feature

* connect cluster strategy (b5cff644f041)
* add method to validate cluster (1ac3d6d29123)
* skip warnings (856cccef3b28)
* move parse from docstyle (8752ec22f0e9)
* move code form docstyle (8dad17ccd9ca)
* use improvement to improve detection (8fa61331eb63)
* move improvement from words (9f2d8c19936a)

## v0.5.0

### Feature

* skip single chapters (58f196584f0f)
* ensure that alignment matches when merge two lines (9f6926b12258)
* connect nolevel strategy (918f3f35f78d)
* move nolevel from words (eee562aab118)
* add finalize to polish result data (5ba8f7dab4a7)
* make runner configurable (3733f927d239)
* add legacy step to produce words compatible result path (3bc8d54940a0)

## v0.4.0

### Feature

* try to merge next line if size matches (0aa818a25308)
* add headline min count (629d864b1f3e)
* use style to cluster headlines (9b8ed3e14474)
* overwrite style level due text level (5ef415641197)
* make after diff max size dependent (212e99e1f9bf)
* use double extractor as default (d98e61dfd1ed)

## v0.3.0

### Feature

* use elements to determine level (9930b9fc7312)
* connect standard headline extractor (0753dd2a09fd)
* move standard from words (422728cf772c)

### Fix

* do not judge result early (1ffb08fd6728)

## v0.2.0

### Feature

* connect numbers large (da0b20698bab)
* move nlarge from words (dff4369ed36c)
* connect strategy (b3ff8e4aae45)
* move single from words (96be5de0802f)

## v0.1.0

### Feature

* add simple decider (82125749d5c3)
* determine pages only once (0ff54f61f1bf)
* shrink headline detection (e9931a5b5955)
* add method to determine pages with expected headlines (8d6289960f90)
* make longest level one length dependent (9f530fded7dd)
* use judger to disable bad results (9b7a39124f58)
* move judger from words (579b6738802d)
* group headlines into expected chapters (65540748e025)
* run strategy with different h1 lower bounds (7192285e93d1)
* make h1 min size adjustable (1417e2607acd)
* connect strategy (7091736613ea)
* add method to run strategy for complete document (cc2d4bfa16f0)
* adjust interface (dbd189bd06c1)
* move code from words (95578f2e88bc)
* move code from words (62e0bc65d7aa)
* move code from words (1a5835b33382)
* move code from words (705ae4c1ed75)
* add feature runner (5bbaade07299)
* add feature package (a0692321b93a)

### Documentation

* add module documentation (6d95f88812d2)

## v0.0.0 Initial release
