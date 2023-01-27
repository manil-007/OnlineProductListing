import React, { useState } from "react";
import {
  Typography,
  TextField,
  Button,
  Stepper,
  Step,
  StepLabel,
} from "@material-ui/core";
import { makeStyles } from "@material-ui/core/styles";
import {
  useForm,
  Controller,
  FormProvider,
  useFormContext,
} from "react-hook-form";
import { DataGrid } from '@mui/x-data-grid';
import Stack from '@mui/material/Stack';

const useStyles = makeStyles((theme) => ({
  button: {
    marginRight: theme.spacing(1),
  },
}));

function getSteps() {
  return [
    "Product Details",
    "Data Generation",
    "Data Updation",
  ];
}
const ProductForm = () => {
  const { control } = useFormContext();
  return (
    
      <Stack
          //component="form"
          sx={{
          width: '100%',
          paddingTop: '5%',
          paddinfBottom: '5%',
          }}
          spacing={3}
          noValidate
          autoComplete="off"
          >
      <Controller
        control={control}
        name="productNames"
        render={({ field }) => (
          <TextField
            id="product-names"
            label="Product Names"
            variant="outlined"
            placeholder="Enter Product Names seperated by semicolon"
            fullWidth
            margin="normal"
            {...field}
          />
        )}
      />

      <Controller
        control={control}
        name="topProducts"
        render={({ field }) => (
          <TextField
            id="top-products"
            label="Top N Products"
            variant="outlined"
            placeholder="Enter Top 'n' Products to be Searched"
            fullWidth
            margin="normal"
            {...field}
          />
        )}
      />
    </Stack>
    
  );
};
const columns = [
  { field: 'id', headerName: 'ASIN', width: 70 },
  { field: 'productName', headerName: 'Product Name', width: 130 },
  { field: 'productTitle', headerName: 'Product Title', width: 200 },
  { field: 'productDescription', headerName: 'Product Description', width: 300 },
  { field: 'keywords', headerName: 'Keywords', width: 200 },
];

const rows = [
  { id: 1, productName: 'Hair Oil', productTitle: 'Best Hair Oil', productDescription: 'Worlds best hair oil for men and women', keywords:'Best hair oil in india'},
  { id: 2, productName: 'Hair Oil', productTitle: 'Best Hair Oil', productDescription: 'Worlds best hair oil for men and women', keywords:'Best hair oil in india'},
  { id: 3, productName: 'Hair Oil', productTitle: 'Best Hair Oil', productDescription: 'Worlds best hair oil for men and women', keywords:'Best hair oil in india'},
  { id: 4, productName: 'Hair Oil', productTitle: 'Best Hair Oil', productDescription: 'Worlds best hair oil for men and women', keywords:'Best hair oil in india'},
];

const UpdateData = () => {
  const { control } = useFormContext();
  return (
    <>
      <Controller
        control={control}
        name="updatedData" 
        render={({ field }) => (
          <div style={{ height: '400', position: 'absolute', top: '40%'}}>
          </div>
        )}
      />
    </>
  );
};
const GeneratedData = () => {
  const { control } = useFormContext();
  return (
    <>
      <Controller
        control={control}
        name="updatedData"
        render={({ field }) => (
        <div style={{ height: 400, width: '100%' }}>
          <DataGrid
            rows={rows}
            columns={columns}
            pageSize={5}
            rowsPerPageOptions={[5]}
            checkboxSelection
          />
        </div>
        )}
      />
    </>
  );
};

function getStepContent(step) {
  switch (step) {
    case 0:
      return <ProductForm />;

    case 1:
      return <GeneratedData />;
    case 2:
      return <UpdateData />;
    default:
      return "unknown step";
  }
}

const LinaerStepper = () => {
  const classes = useStyles();
  const methods = useForm({
    defaultValues: {
      productNames: "",
      topProducts: "",
      generatedData: "",
    },
  });
  const [activeStep, setActiveStep] = useState(0);
  const [skippedSteps, setSkippedSteps] = useState([]);
  const steps = getSteps();

  const isStepOptional = (step) => {
    return step === 4 || step === 5;
  };

  const isStepSkipped = (step) => {
    return skippedSteps.includes(step);
  };

  const handleNext = (data) => {
    console.log(data);
    if (activeStep === steps.length - 1) {
      console.log(data);
      setActiveStep(activeStep + 1);
    } else {
      setActiveStep(activeStep + 1);
      setSkippedSteps(
        skippedSteps.filter((skipItem) => skipItem !== activeStep)
      );
    }
  };

  const handleBack = () => {
    setActiveStep(activeStep - 1);
  };

  const handleSkip = () => {
    if (!isStepSkipped(activeStep)) {
      setSkippedSteps([...skippedSteps, activeStep]);
    }
    setActiveStep(activeStep + 1);
  };

  // const onSubmit = (data) => {
  //   console.log(data);
  // };
  return (
    <div>
      <Stepper alternativeLabel activeStep={activeStep}>
        {steps.map((step, index) => {
          const labelProps = {};
          const stepProps = {};
          if (isStepOptional(index)) {
            labelProps.optional = (
              <Typography
                variant="caption"
                align="center"
                style={{ display: "block" }}
              >
                optional
              </Typography>
            );
          }
          if (isStepSkipped(index)) {
            stepProps.completed = false;
          }
          return (
            <Step {...stepProps} key={index}>
              <StepLabel {...labelProps}>{step}</StepLabel>
            </Step>
          );
        })}
      </Stepper>

      {activeStep === steps.length ? (
        <Typography variant="h3" align="center">
          Thank You
        </Typography>
      ) : (
        <>
          <FormProvider {...methods}>
            <form onSubmit={methods.handleSubmit(handleNext)}>
              {getStepContent(activeStep)}

              <Button
                className={classes.button}
                disabled={activeStep === 0}
                onClick={handleBack}
              >
                back
              </Button>
              {isStepOptional(activeStep) && (
                <Button
                  className={classes.button}
                  variant="contained"
                  color="primary"
                  onClick={handleSkip}
                >
                  skip
                </Button>
              )}
              <Button
                className={classes.button}
                variant="contained"
                color="primary"
                // onClick={handleNext}
                type="submit"
              >
                {activeStep === steps.length - 1 ? "Finish" : "Next"}
              </Button>
            </form>
          </FormProvider>
        </>
      )}
    </div>
  );
};

export default LinaerStepper;
