CREATE MIGRATION m17wta2dxiakrf4vwxhpbuabmxrsqjolskwpxlvjrnirmt2w6q2kwa
    ONTO m1gneroa67coilsqbknpo43tnjk7dpkkczo43rmzntoxisi5jmo4nq
{
  ALTER TYPE default::Article {
      ALTER PROPERTY time_elascate {
          RENAME TO duration;
      };
  };
};
