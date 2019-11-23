/// <reference types="Cypress" />

context('Registration', () => {
  it('Page exists for creating users', () => {
    cy.visit('127.0.0.1:5000/createuser')
  })
  it('Contains input fields for username and password', () => {
    cy.get('input#username')
    cy.get('input#password')
  })
  it('Requires 8 character password', () => {
    cy.visit('127.0.0.1:5000/createuser')
    cy.get('input#username').clear().type('test')
    cy.get('input#password').clear().type('pass')
    cy.get('input#submit').click()
    cy.get('p#message').contains('Password too short')
  })
  it('Requires a unique username', () => {
    cy.visit('127.0.0.1:5000/createuser')
    cy.get('input#username').clear().type('admin')
    cy.get('input#password').clear().type('password')
    cy.get('input#submit').click()
    cy.get('p#message').contains('User already exists')
  })
})
