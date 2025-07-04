CREATE MIGRATION m1fypbbbrcytnblrof5i66llwth6xqdtffvurtayhkzba2o2glvoaq
    ONTO m1n75zblvvugpvmfjcpfbzuyf4na2r5fm4q2jz5rgwn2yyyewrbndq
{
  CREATE SCALAR TYPE default::DegreeNames EXTENDING enum<ASSOCIATES_DEGREE, BACHELORS_DEGREE, MASTERS_DEGREE, DOCTORAL_DEGREE>;
  ALTER TYPE default::DateTime {
      ALTER PROPERTY updated_at {
          CREATE REWRITE
              UPDATE 
              USING (std::datetime_current());
      };
  };
  CREATE TYPE default::Degree EXTENDING default::DateTime {
      CREATE REQUIRED PROPERTY name: default::DegreeNames;
  };
  ALTER TYPE default::University {
      CREATE MULTI LINK degree: default::Degree;
      CREATE REQUIRED PROPERTY featured: std::bool {
          SET default := false;
      };
      CREATE PROPERTY rating: std::float64;
      CREATE PROPERTY url: std::str;
  };
};
