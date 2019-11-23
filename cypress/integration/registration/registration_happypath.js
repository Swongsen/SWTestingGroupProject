/// <reference types="Cypress" />

context('Registration', () => {
  it('Page exists for creating users', () => {
    cy.visit('127.0.0.1:5000/createuser')
  })
  it('Contains input fields for username and password', () => {
    cy.get('input#username')
    cy.get('input#password')
  })
  it('Can make a new user with appropriate credentials', () => {
    var date = new Date()
    var current_time = date.getTime()
    var current_time_string = current_time.toString()
    cy.visit('127.0.0.1:5000/createuser')
    cy.get('input#username').clear().type('test'+current_time_string)
    cy.get('input#password').clear().type('password'+current_time_string)
    cy.get('input#submit').click()
    cy.get('p#message').contains('User successfully created')
  })
})
