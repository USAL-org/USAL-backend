CREATE MIGRATION m1ivlhbckdpn3br3kamadapyeerztpcl2qgozpeg62oecuk35b5cha
    ONTO m1bourgyhuxfmxh6ohxg4iobc6zzwxhwb4pawi4unr4wfwg3xizlzq
{
  ALTER TYPE default::Major {
      DROP PROPERTY description;
  };
};
