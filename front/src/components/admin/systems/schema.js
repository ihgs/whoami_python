import VueFormGenerator from 'vue-form-generator'
const validators = VueFormGenerator.validators
const system = {
  fields: [
    {
      type: 'input',
      name: 'SystemName',
      inputType: 'text',
      label: 'System Name',
      model: 'name',
      validator: [validators.string],
      required: true
    },
    {
      type: 'input',
      name: 'URL',
      inputType: 'text',
      label: 'System URL',
      model: 'url',
      validator: [validators.string],
      required: true
    }
  ]
}

export default { system }
