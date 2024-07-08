import { Grid, Typography } from '@mui/material';

const PollNumbResultOut = ({ data, res }) => {
  const renderItem = (item, value, bold = false) => (
    <Grid item xs={bold ? 10 : 2} sx={{ padding: '2px' }}>
      <Typography sx={{ fontSize: '13px', fontWeight: bold ? 'bold' : 'normal' }}>
        {value}
      </Typography>
    </Grid>
  );

  return data.map((item) => (
    <>
      {renderItem(item, item.caption, true)}
      {renderItem(item, res[item.field])}
    </>
  ));
};

export default PollNumbResultOut;
