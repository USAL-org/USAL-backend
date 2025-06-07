CREATE MIGRATION m1sd6zju2sd5r6cu43bwvtcciwawdyumppuhiekj6ydibpdqkfhhaq
    ONTO m1nxk2bhhhhzxb5b7ejmxdnda64mjxuj4dakjsa4bwpuzetbrjlzbq
{
  CREATE TYPE default::OTP EXTENDING default::DateTime {
      CREATE LINK user: default::User;
      CREATE REQUIRED PROPERTY expiration_time: std::datetime;
      CREATE REQUIRED PROPERTY secret: std::str;
  };
};
