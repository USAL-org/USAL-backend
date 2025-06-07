CREATE MIGRATION m1wur5ksz2zmuvx54uxcq56cvkuyhdz3inysspserxx2s6t5ypm6eq
    ONTO m1sd6zju2sd5r6cu43bwvtcciwawdyumppuhiekj6ydibpdqkfhhaq
{
  ALTER TYPE default::User {
      ALTER PROPERTY first_name {
          RENAME TO full_name;
      };
  };
  ALTER TYPE default::User {
      DROP PROPERTY last_name;
      DROP PROPERTY middle_name;
  };
};
