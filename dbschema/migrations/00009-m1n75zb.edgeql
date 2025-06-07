CREATE MIGRATION m1n75zblvvugpvmfjcpfbzuyf4na2r5fm4q2jz5rgwn2yyyewrbndq
    ONTO m1wur5ksz2zmuvx54uxcq56cvkuyhdz3inysspserxx2s6t5ypm6eq
{
  CREATE TYPE default::DefaultSha EXTENDING default::DateTime {
      CREATE REQUIRED PROPERTY hash: std::str;
      CREATE REQUIRED PROPERTY key: std::str;
  };
};
