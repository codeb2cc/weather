"use strict"

describe('Karma Test', function () {
  var module

  beforeEach(function () {
    module = angular.module('weather')
  })
  afterEach(function () {})

  it('AngularJS module test', function () {
    expect(module).not.toEqual(null)
  })
})

